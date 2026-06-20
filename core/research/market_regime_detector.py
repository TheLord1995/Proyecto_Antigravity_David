"""
Detector determinista de régimen de mercado basado en velas OHLCV.

Responsabilidad:
OHLCV candles -> cálculo técnico simple -> MarketRegimeResult

Métricas utilizadas:
- ATR (Average True Range): rango medio real de las velas.
- ATR%: ATR normalizado como porcentaje del precio de cierre.
- Trend Efficiency (Efficiency Ratio de Kaufman): mide la eficiencia
  direccional del precio. Rango 0-100. NO es ADX de Welles Wilder.
  Fórmula: |close_final - close_inicial| / Σ|close_i - close_{i-1}| × 100
- Volatility%: desviación media absoluta de cierres normalizada.

No ejecuta operaciones.
No aprueba operativa real.
No sustituye al RiskEngine.
"""

from core.research.market_regime_models import (
    MarketRegime,
    MarketRegimeResult,
    OHLCVRecord,
)


class MarketRegimeDetector:
    MIN_CANDLES = 30

    TREND_EFFICIENCY_TRENDING_THRESHOLD = 30.0
    TREND_EFFICIENCY_RANGING_THRESHOLD = 15.0

    HIGH_ATR_PCT_THRESHOLD = 2.5
    LOW_ATR_PCT_THRESHOLD = 0.4

    LOW_VOLATILITY_PCT_THRESHOLD = 0.5

    VOLATILITY_LOOKBACK = 20

    def detect(self, candles: list[OHLCVRecord]) -> MarketRegimeResult:
        candles_copy = list(candles)
        candles_analyzed = len(candles_copy)

        if candles_analyzed < self.MIN_CANDLES:
            return MarketRegimeResult(
                regime=MarketRegime.INSUFFICIENT_DATA,
                confidence=1.0,
                trend_efficiency=None,
                atr=None,
                atr_pct=None,
                volatility_pct=None,
                candles_analyzed=candles_analyzed,
                reason="Datos insuficientes para detectar régimen de mercado.",
                approved_for_real=False,
            )

        atr = self._calculate_atr(candles_copy)
        atr_pct = self._calculate_atr_pct(atr, candles_copy[-1].close)
        trend_efficiency = self._calculate_trend_efficiency(candles_copy)
        volatility_pct = self._calculate_volatility_pct(candles_copy)

        if atr_pct >= self.HIGH_ATR_PCT_THRESHOLD:
            return MarketRegimeResult(
                regime=MarketRegime.HIGH_VOLATILITY,
                confidence=0.85,
                trend_efficiency=trend_efficiency,
                atr=atr,
                atr_pct=atr_pct,
                volatility_pct=volatility_pct,
                candles_analyzed=candles_analyzed,
                reason="ATR porcentual elevado detectado.",
                approved_for_real=False,
            )

        if trend_efficiency >= self.TREND_EFFICIENCY_TRENDING_THRESHOLD:
            return MarketRegimeResult(
                regime=MarketRegime.TRENDING,
                confidence=0.80,
                trend_efficiency=trend_efficiency,
                atr=atr,
                atr_pct=atr_pct,
                volatility_pct=volatility_pct,
                candles_analyzed=candles_analyzed,
                reason="Eficiencia de tendencia elevada detectada.",
                approved_for_real=False,
            )

        if trend_efficiency < self.TREND_EFFICIENCY_RANGING_THRESHOLD:
            return MarketRegimeResult(
                regime=MarketRegime.RANGING,
                confidence=0.75,
                trend_efficiency=trend_efficiency,
                atr=atr,
                atr_pct=atr_pct,
                volatility_pct=volatility_pct,
                candles_analyzed=candles_analyzed,
                reason="Eficiencia de tendencia baja compatible con mercado lateral.",
                approved_for_real=False,
            )

        if (
            atr_pct <= self.LOW_ATR_PCT_THRESHOLD
            or volatility_pct <= self.LOW_VOLATILITY_PCT_THRESHOLD
        ):
            return MarketRegimeResult(
                regime=MarketRegime.LOW_VOLATILITY,
                confidence=0.80,
                trend_efficiency=trend_efficiency,
                atr=atr,
                atr_pct=atr_pct,
                volatility_pct=volatility_pct,
                candles_analyzed=candles_analyzed,
                reason="Volatilidad baja detectada por ATR porcentual o dispersión de cierres.",
                approved_for_real=False,
            )

        return MarketRegimeResult(
            regime=MarketRegime.MIXED,
            confidence=0.60,
            trend_efficiency=trend_efficiency,
            atr=atr,
            atr_pct=atr_pct,
            volatility_pct=volatility_pct,
            candles_analyzed=candles_analyzed,
            reason="Señales técnicas no concluyentes.",
            approved_for_real=False,
        )

    def _calculate_atr(self, candles: list[OHLCVRecord], period: int = 14) -> float:
        true_ranges: list[float] = []

        for index in range(1, len(candles)):
            current = candles[index]
            previous = candles[index - 1]

            true_range = max(
                current.high - current.low,
                abs(current.high - previous.close),
                abs(current.low - previous.close),
            )
            true_ranges.append(true_range)

        selected_ranges = true_ranges[-period:]
        return sum(selected_ranges) / len(selected_ranges)

    def _calculate_atr_pct(self, atr: float, close: float) -> float:
        return (atr / close) * 100

    def _calculate_trend_efficiency(
        self, candles: list[OHLCVRecord], period: int = 14
    ) -> float:
        """
        Calcula el Efficiency Ratio de Kaufman (ER) escalado a 0-100.

        NO es el ADX de Welles Wilder. El ER mide la relación entre el
        movimiento neto y el movimiento total usando solo precios de cierre.

        ER = |close_final - close_inicial| / Σ|close_i - close_{i-1}| × 100

        - ER = 100: tendencia perfecta (línea recta).
        - ER = 0: mercado lateral puro (movimiento neto cero).
        """
        selected = candles[-period:]

        first_close = selected[0].close
        last_close = selected[-1].close

        net_movement = abs(last_close - first_close)

        total_movement = 0.0
        for index in range(1, len(selected)):
            total_movement += abs(selected[index].close - selected[index - 1].close)

        if total_movement == 0:
            return 0.0

        trend_efficiency = net_movement / total_movement

        return min(trend_efficiency * 100, 100.0)

    def _calculate_volatility_pct(self, candles: list[OHLCVRecord]) -> float:
        selected = candles[-self.VOLATILITY_LOOKBACK :]
        closes = [candle.close for candle in selected]

        average_close = sum(closes) / len(closes)
        mean_absolute_deviation = sum(
            abs(close - average_close) for close in closes
        ) / len(closes)

        return (mean_absolute_deviation / average_close) * 100