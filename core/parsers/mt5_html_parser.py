"""
core/parsers/mt5_html_parser.py
--------------------------------
Implementación concreta del parser para informes HTML de MetaTrader 5 en inglés y español.
Fase 4.1: Import Layer — Única implementación autorizada en esta fase.

Responsabilidades:
  - Leer archivos HTML locales generados por MT5 (soporta codificación UTF-8 y UTF-16LE).
  - Validar que el idioma sea inglés o español.
  - Validar que la estructura sea reconocible como un informe MT5.
  - Extraer métricas directamente del DOM utilizando alias bilingües.
  - Calcular el hash SHA-256 del archivo original.
  - Construir y retornar un objeto BacktestReport Pydantic.

Sin red. Sin MT5 en vivo. Sin base de datos. Sin ejecución real.
"""

import re
from typing import Optional

from bs4 import BeautifulSoup

from core.parsers.base_parser import BaseParser, ParserLanguageError, ParserStructureError
from core.strategy_models import BacktestPeriod, BacktestReport

# ─── ANCLAS DE IDENTIDAD MT5 BILINGÜES ───────────────────────────────────────
# Cadenas que confirman la identidad de un informe de MetaTrader 5 en inglés o español.
_CRITICAL_ANCHORS = {
    "Profit factor": ["Profit factor", "Factor de Beneficio", "Factor de beneficio"],
    "Total trades": ["Total trades", "Total de operaciones ejecutadas", "Total de transacciones"],
    "Maximal drawdown": ["Maximal drawdown", "Reducción máxima del balance", "Reducción máxima de la equidad", "Caída máxima"],
}

# Cadenas que indican que el informe está en un idioma no soportado.
_UNSUPPORTED_LANGUAGE_INDICATORS = [
    "Facteur de profit",
    "Gewinnfaktor",
]

# Diccionario de alias bilingües para extracción de métricas.
_METRIC_ALIASES = {
    "total_trades": ["Total de operaciones ejecutadas", "Total de transacciones", "Total trades"],
    "profit_factor": ["Factor de Beneficio", "Factor de beneficio", "Profit factor"],
    "recovery_factor": ["Factor de Recuperación", "Factor de recuperación", "Recovery factor"],
    "sharpe_ratio": ["Ratio de Sharpe", "Ratio de sharpe", "Sharpe ratio"],
    "expectancy": ["Beneficio Esperado", "Beneficio esperado", "Expected payoff"],
    "average_win": ["Promedio de transacción rentable", "Promedio de transacción rentable:", "Average profit trade"],
    "average_loss": ["Promedio de transacción no rentable", "Promedio de transacción no rentable:", "Average loss trade"],
    "max_losing_streak": ["El número máximo de pérdidas consecutivas", "El máximo de pérdidas consecutivas", "Maximum consecutive losses"],
    "net_profit": ["Beneficio Neto", "Total net profit", "Beneficio neto total"],
    "gross_profit": ["Beneficio Bruto", "Gross profit"],
    "gross_loss": ["Pérdidas Brutas", "Gross loss"],
}

_DRAWDOWN_ALIASES = [
    "Maximal drawdown",
    "Reducción máxima del balance",
    "Reducción máxima de la equidad",
    "Caída máxima",
]

_WIN_RATE_PATTERNS = [
    r"Profit trades[\s\S]*?\((\d+[\.,]\d+)%\)",
    r"Posiciones rentables[\s\S]*?\((\d+[\.,]\d+)%\)",
    r"Operaciones rentables[\s\S]*?\((\d+[\.,]\d+)%\)",
]


class MT5HtmlParser(BaseParser):
    """
    Parser determinista para informes HTML de MetaTrader 5 generados en inglés y español.

    Lanza:
        ParserLanguageError:  Si el informe está en un idioma distinto a inglés o español.
        ParserStructureError: Si el HTML no corresponde a un informe MT5.
        FileNotFoundError:    Si el archivo no existe.
    """

    def parse(
        self,
        file_path: str,
        strategy_id: str,
        version: str,
        is_period: BacktestPeriod,
        oos_period: BacktestPeriod,
    ) -> BacktestReport:
        """
        Parsea un informe HTML de MT5 en inglés o español y retorna un BacktestReport.
        """
        # ── 1. LEER ARCHIVO LOCAL ─────────────────────────────────────────────
        raw_html = self._read_file(file_path)

        # ── 2. CALCULAR HASH SHA-256 ANTES DE CUALQUIER MODIFICACIÓN ──────────
        source_hash = self._calculate_file_hash(file_path)

        # ── 3. CONSTRUIR DOM ──────────────────────────────────────────────────
        soup = BeautifulSoup(raw_html, "lxml")
        full_text = soup.get_text()

        # ── 4. VALIDAR IDIOMA ─────────────────────────────────────────────────
        self._validate_language(full_text)

        # ── 5. VALIDAR ESTRUCTURA MT5 ─────────────────────────────────────────
        self._validate_mt5_structure(full_text)

        # ── 6. EXTRAER MÉTRICAS ───────────────────────────────────────────────
        metrics = self._extract_metrics(soup, full_text)

        # ── 7. CONSTRUIR Y RETORNAR BacktestReport ────────────────────────────
        return BacktestReport(
            strategy_id=strategy_id,
            version=version,
            data_source="MetaTrader 5 HTML",
            in_sample_period=is_period,
            out_of_sample_period=oos_period,
            total_trades=metrics["total_trades"],
            profit_factor_is=metrics["profit_factor_is"],
            profit_factor_oos=metrics["profit_factor_oos"],
            max_drawdown_pct=metrics["max_drawdown_pct"],
            recovery_factor=metrics["recovery_factor"],
            sharpe_ratio=metrics["sharpe_ratio"],
            sortino_ratio=0.0,           # Requiere Metrics Engine (Fase futura)
            expectancy=metrics["expectancy"],
            average_win=metrics["average_win"],
            average_loss=metrics["average_loss"],
            win_rate=metrics["win_rate"],
            max_losing_streak=metrics["max_losing_streak"],
            max_daily_loss_pct=0.0,      # Requiere análisis trade-by-trade (Fase futura)
            simultaneous_exposure_pct=0.0,  # Requiere análisis temporal (Fase futura)
            risk_of_ruin_pct=0.0,        # Requiere Monte Carlo (Fase futura)
            average_slippage=0.0,        # No disponible en cabecera HTML
            average_trade_cost=0.0,      # No disponible en cabecera HTML
            raw_metrics={
                "source_file_hash": source_hash,
                "parser": "MT5HtmlParser-V1",
                **metrics,
            },
        )

    # ─── MÉTODOS PRIVADOS ─────────────────────────────────────────────────────

    def _read_file(self, file_path: str) -> str:
        """Lee el archivo HTML local. Lanza FileNotFoundError si no existe."""
        try:
            with open(file_path, "rb") as f:
                raw = f.read()
            # Detección de BOM de UTF-16
            encoding = "utf-16" if raw[:2] in (b"\xff\xfe", b"\xfe\xff") else "utf-8"
            return raw.decode(encoding, errors="replace")
        except FileNotFoundError:
            raise FileNotFoundError(
                f"[MT5HtmlParser] Archivo no encontrado: {file_path}"
            )

    def _validate_language(self, text: str) -> None:
        """
        Rechaza el informe si contiene indicadores de idiomas no soportados.
        """
        for indicator in _UNSUPPORTED_LANGUAGE_INDICATORS:
            if indicator in text:
                raise ParserLanguageError(
                    f"[MT5HtmlParser] Informe rechazado: idioma no inglés/español detectado "
                    f"(encontrado: '{indicator}'). "
                    "MT5 reports must be generated in English or Spanish."
                )

    def _validate_mt5_structure(self, text: str) -> None:
        """
        Verifica que el HTML contenga al menos una de las cadenas ancla para
        cada una de las categorías críticas de un informe MT5 válido.
        Si alguna falta, se lanza ParserStructureError.
        """
        for name, aliases in _CRITICAL_ANCHORS.items():
            if not any(alias.lower() in text.lower() for alias in aliases):
                raise ParserStructureError(
                    f"[MT5HtmlParser] Estructura MT5 no reconocida. "
                    f"Etiqueta crítica no encontrada: '{name}' (alias buscados: {aliases}). "
                    "El archivo puede no ser un informe de MetaTrader 5 válido."
                )

    def _extract_metrics(self, soup: BeautifulSoup, text: str) -> dict:
        """
        Extrae las métricas disponibles directamente del DOM HTML del informe MT5.
        Lanza ParserStructureError si falta alguna métrica crítica.
        """
        # Métricas críticas
        total_trades = self._extract_int_from_aliases(text, _METRIC_ALIASES["total_trades"], "Total trades")
        profit_factor_is = self._extract_float_from_aliases(text, _METRIC_ALIASES["profit_factor"], "Profit factor")
        # Compatibilidad estructural:
# un informe MT5 estándar no separa automáticamente In Sample / Out of Sample.
# Por tanto, profit_factor_oos replica temporalmente profit_factor_is.
# La separación IS/OOS deberá resolverse en una fase posterior mediante
# particionado explícito del dataset o metadatos externos del backtest.
        
        profit_factor_oos = profit_factor_is
        max_drawdown_pct = self._extract_drawdown_pct_from_aliases(text, _DRAWDOWN_ALIASES)

        # Métricas no críticas (fallback a 0.0 o 0)
        recovery_factor = self._extract_float_from_aliases(text, _METRIC_ALIASES["recovery_factor"])
        sharpe_ratio = self._extract_float_from_aliases(text, _METRIC_ALIASES["sharpe_ratio"])
        expectancy = self._extract_float_from_aliases(text, _METRIC_ALIASES["expectancy"])
        average_win = self._extract_float_from_aliases(text, _METRIC_ALIASES["average_win"])
        average_loss = abs(self._extract_float_from_aliases(text, _METRIC_ALIASES["average_loss"]))
        win_rate = self._extract_win_rate_from_patterns(text, _WIN_RATE_PATTERNS)
        max_losing_streak = self._extract_int_from_aliases(text, _METRIC_ALIASES["max_losing_streak"])

        # Opcionales bilingües solicitadas por el usuario
        net_profit = self._extract_float_from_aliases(text, _METRIC_ALIASES["net_profit"])
        gross_profit = self._extract_float_from_aliases(text, _METRIC_ALIASES["gross_profit"])
        gross_loss = self._extract_float_from_aliases(text, _METRIC_ALIASES["gross_loss"])

        return {
            "total_trades": total_trades,
            "profit_factor_is": profit_factor_is,
            "profit_factor_oos": profit_factor_oos,
            "max_drawdown_pct": max_drawdown_pct,
            "recovery_factor": recovery_factor,
            "sharpe_ratio": sharpe_ratio,
            "expectancy": expectancy,
            "average_win": average_win,
            "average_loss": average_loss,
            "win_rate": win_rate,
            "max_losing_streak": max_losing_streak,
            "net_profit": net_profit,
            "gross_profit": gross_profit,
            "gross_loss": gross_loss,
        }

    def _extract_float_from_aliases(self, text: str, aliases: list[str], critical_name: str = None) -> float:
        """
        Busca en el texto la primera coincidencia de un alias y extrae
        el valor numérico inmediatamente siguiente.
        """
        for alias in aliases:
            pattern = re.compile(
                re.escape(alias) + r"[^\d\-]*?([\-]?\d[\d\s]*[\.,]?\d*)",
                re.IGNORECASE,
            )
            match = pattern.search(text)
            if match:
                return self._to_float(match.group(1))
        if critical_name:
            raise ParserStructureError(
                f"[MT5HtmlParser] Métrica crítica no encontrada: '{critical_name}'. "
                f"El informe no contiene ninguna de las etiquetas asociadas: {aliases}"
            )
        return 0.0

    def _extract_int_from_aliases(self, text: str, aliases: list[str], critical_name: str = None) -> int:
        """
        Busca en el texto la primera coincidencia de un alias y extrae
        el valor entero inmediatamente siguiente.
        """
        for alias in aliases:
            pattern = re.compile(
                re.escape(alias) + r"[^\d]*?(\d+)",
                re.IGNORECASE,
            )
            match = pattern.search(text)
            if match:
                return int(match.group(1).replace(" ", ""))
        if critical_name:
            raise ParserStructureError(
                f"[MT5HtmlParser] Métrica crítica no encontrada: '{critical_name}'. "
                f"El informe no contiene ninguna de las etiquetas asociadas: {aliases}"
            )
        return 0

    def _extract_drawdown_pct_from_aliases(self, text: str, aliases: list[str]) -> float:
        """
        Extrae el drawdown relativo (%) de la primera coincidencia de alias.
        MT5 lo reporta en formato: 'Maximal drawdown   1234.56 (12.34%)'
        """
        for alias in aliases:
            pattern = re.compile(
                re.escape(alias) + r"[^\d]*[\d\s\.,]+\(([\d\.,]+)%\)",
                re.IGNORECASE,
            )
            match = pattern.search(text)
            if match:
                return self._to_float(match.group(1))
            # Fallback: intentar extraer cualquier float tras el alias
            pattern_fallback = re.compile(
                re.escape(alias) + r"[^\d\-]*?([\-]?\d[\d\s]*[\.,]?\d*)",
                re.IGNORECASE,
            )
            match_fb = pattern_fallback.search(text)
            if match_fb:
                return self._to_float(match_fb.group(1))
        raise ParserStructureError(
            f"[MT5HtmlParser] Métrica crítica no encontrada: 'Maximal drawdown'. "
            f"El informe no contiene ninguna de las etiquetas asociadas: {aliases}"
        )

    def _extract_win_rate_from_patterns(self, text: str, patterns: list[str]) -> float:
        """
        Extrae el Win Rate utilizando expresiones regulares.
        Retorna el valor como decimal (ej. 76.67 -> 76.67, NO 0.7667).
        """
        for pattern_str in patterns:
            pattern = re.compile(pattern_str, re.IGNORECASE)
            match = pattern.search(text)
            if match:
                return self._to_float(match.group(1))
        return 0.0

    @staticmethod
    def _to_float(value: str) -> float:
        """Normaliza un string numérico (comas/espacios) a float."""
        try:
            return float(value.replace(" ", "").replace(",", "."))
        except (ValueError, AttributeError):
            return 0.0
