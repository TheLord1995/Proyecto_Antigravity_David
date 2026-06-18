"""
core/research/regime_performance_analyzer.py
--------------------------------------------
Analizador determinista de rendimiento por régimen de mercado.

No ejecuta operaciones.
No aprueba operativa real.
No sustituye al RiskEngine.
"""

from typing import Any

from core.research.base_research_validator import BaseResearchValidator
from core.research.research_models import (
    ResearchFinding,
    ResearchFindingSeverity,
    ResearchValidationInput,
)


class RegimePerformanceAnalyzer(BaseResearchValidator):
    """Evalúa si una estrategia mantiene rendimiento aceptable por régimen."""

    METADATA_KEY = "regime_performance"

    MIN_TRADES_PER_REGIME = 30
    MIN_PROFIT_FACTOR_PER_REGIME = 1.10
    MIN_EXPECTANCY_PER_REGIME = 0.0
    MAX_DRAWDOWN_PER_REGIME_PCT = 30.0

    def analyze(self, data: ResearchValidationInput) -> list[ResearchFinding]:
        findings: list[ResearchFinding] = []

        regime_performance = data.metadata.get(self.METADATA_KEY)

        if not regime_performance:
            findings.append(
                ResearchFinding(
                    code="NO_REGIME_PERFORMANCE_DATA",
                    severity=ResearchFindingSeverity.WARNING,
                    component="regime_performance",
                    message="No se han declarado métricas de rendimiento separadas por régimen de mercado.",
                    evidence={"metadata_key": self.METADATA_KEY},
                )
            )
            return findings

        if not isinstance(regime_performance, dict):
            findings.append(
                ResearchFinding(
                    code="INVALID_REGIME_PERFORMANCE_FORMAT",
                    severity=ResearchFindingSeverity.CRITICAL,
                    component="regime_performance",
                    message="El rendimiento por régimen debe declararse como un diccionario.",
                    evidence={"received_type": type(regime_performance).__name__},
                )
            )
            return findings

        for regime, metrics in regime_performance.items():
            if not isinstance(metrics, dict):
                findings.append(
                    ResearchFinding(
                        code="INVALID_REGIME_METRICS_FORMAT",
                        severity=ResearchFindingSeverity.CRITICAL,
                        component="regime_performance",
                        message="Las métricas de cada régimen deben declararse como un diccionario.",
                        evidence={
                            "regime": regime,
                            "received_type": type(metrics).__name__,
                        },
                    )
                )
                continue

            findings.extend(
                self._analyze_single_regime(
                    regime=str(regime),
                    metrics=metrics,
                )
            )

        if not findings:
            findings.append(
                ResearchFinding(
                    code="REGIME_PERFORMANCE_OK",
                    severity=ResearchFindingSeverity.INFO,
                    component="regime_performance",
                    message="La estrategia mantiene métricas aceptables en los regímenes declarados.",
                    evidence={
                        "analyzed_regimes": sorted(regime_performance.keys()),
                    },
                )
            )

        return findings

    def _analyze_single_regime(
        self,
        regime: str,
        metrics: dict[str, Any],
    ) -> list[ResearchFinding]:
        findings: list[ResearchFinding] = []

        trades = metrics.get("trades")
        profit_factor = metrics.get("profit_factor")
        expectancy = metrics.get("expectancy")
        max_drawdown_pct = metrics.get("max_drawdown_pct")

        if trades is None:
            findings.append(
                ResearchFinding(
                    code="REGIME_TRADES_MISSING",
                    severity=ResearchFindingSeverity.WARNING,
                    component="regime_performance",
                    message="Falta el número de operaciones para un régimen de mercado.",
                    evidence={"regime": regime},
                )
            )
        elif trades < self.MIN_TRADES_PER_REGIME:
            findings.append(
                ResearchFinding(
                    code="REGIME_LOW_TRADE_COUNT",
                    severity=ResearchFindingSeverity.WARNING,
                    component="regime_performance",
                    message="El régimen tiene pocas operaciones para una lectura estadística fiable.",
                    evidence={
                        "regime": regime,
                        "trades": trades,
                        "minimum_required": self.MIN_TRADES_PER_REGIME,
                    },
                )
            )

        if profit_factor is None:
            findings.append(
                ResearchFinding(
                    code="REGIME_PROFIT_FACTOR_MISSING",
                    severity=ResearchFindingSeverity.WARNING,
                    component="regime_performance",
                    message="Falta el Profit Factor para un régimen de mercado.",
                    evidence={"regime": regime},
                )
            )
        elif profit_factor < self.MIN_PROFIT_FACTOR_PER_REGIME:
            findings.append(
                ResearchFinding(
                    code="REGIME_LOW_PROFIT_FACTOR",
                    severity=ResearchFindingSeverity.WARNING,
                    component="regime_performance",
                    message="El Profit Factor del régimen está por debajo del mínimo aceptable.",
                    evidence={
                        "regime": regime,
                        "profit_factor": profit_factor,
                        "minimum_required": self.MIN_PROFIT_FACTOR_PER_REGIME,
                    },
                )
            )

        if expectancy is None:
            findings.append(
                ResearchFinding(
                    code="REGIME_EXPECTANCY_MISSING",
                    severity=ResearchFindingSeverity.WARNING,
                    component="regime_performance",
                    message="Falta la esperanza matemática para un régimen de mercado.",
                    evidence={"regime": regime},
                )
            )
        elif expectancy <= self.MIN_EXPECTANCY_PER_REGIME:
            findings.append(
                ResearchFinding(
                    code="REGIME_NON_POSITIVE_EXPECTANCY",
                    severity=ResearchFindingSeverity.CRITICAL,
                    component="regime_performance",
                    message="La esperanza matemática del régimen no es positiva.",
                    evidence={
                        "regime": regime,
                        "expectancy": expectancy,
                        "minimum_required": self.MIN_EXPECTANCY_PER_REGIME,
                    },
                )
            )

        if max_drawdown_pct is None:
            findings.append(
                ResearchFinding(
                    code="REGIME_DRAWDOWN_MISSING",
                    severity=ResearchFindingSeverity.WARNING,
                    component="regime_performance",
                    message="Falta el drawdown máximo para un régimen de mercado.",
                    evidence={"regime": regime},
                )
            )
        elif max_drawdown_pct > self.MAX_DRAWDOWN_PER_REGIME_PCT:
            findings.append(
                ResearchFinding(
                    code="REGIME_DRAWDOWN_TOO_HIGH",
                    severity=ResearchFindingSeverity.WARNING,
                    component="regime_performance",
                    message="El drawdown del régimen es demasiado elevado.",
                    evidence={
                        "regime": regime,
                        "max_drawdown_pct": max_drawdown_pct,
                        "maximum_allowed": self.MAX_DRAWDOWN_PER_REGIME_PCT,
                    },
                )
            )

        return findings