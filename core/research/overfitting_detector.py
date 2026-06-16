"""
core/research/overfitting_detector.py
-------------------------------------
Detector determinista de señales de sobreoptimización.

No ejecuta operaciones.
No aprueba operativa real.
No sustituye al RiskEngine.
"""
from core.research.base_research_validator import BaseResearchValidator
from core.research.research_models import (
    ResearchFinding,
    ResearchFindingSeverity,
    ResearchValidationInput,
)


class OverfittingDetector(BaseResearchValidator):
    """Detecta señales básicas de overfitting en un backtest."""

    MIN_TRADES = 100
    SUSPICIOUS_PROFIT_FACTOR = 2.5
    MAX_IS_OOS_PF_GAP = 0.50

    def analyze(self, data: ResearchValidationInput) -> list[ResearchFinding]:
        findings: list[ResearchFinding] = []

        if not data.has_out_of_sample:
            findings.append(
                ResearchFinding(
                    code="NO_OOS",
                    severity=ResearchFindingSeverity.CRITICAL,
                    component="overfitting",
                    message="La estrategia no incluye validación Out of Sample.",
                    evidence={"has_out_of_sample": data.has_out_of_sample},
                )
            )

        if data.total_trades < self.MIN_TRADES:
            findings.append(
                ResearchFinding(
                    code="LOW_TRADE_COUNT",
                    severity=ResearchFindingSeverity.WARNING,
                    component="overfitting",
                    message="El número de operaciones es bajo para una validación estadística robusta.",
                    evidence={
                        "total_trades": data.total_trades,
                        "minimum_required": self.MIN_TRADES,
                    },
                )
            )

        if (
            data.profit_factor_is is not None
            and data.profit_factor_oos is not None
            and data.profit_factor_is - data.profit_factor_oos > self.MAX_IS_OOS_PF_GAP
        ):
            findings.append(
                ResearchFinding(
                    code="IS_OOS_PF_GAP",
                    severity=ResearchFindingSeverity.WARNING,
                    component="overfitting",
                    message="El Profit Factor In Sample es demasiado superior al Out of Sample.",
                    evidence={
                        "profit_factor_is": data.profit_factor_is,
                        "profit_factor_oos": data.profit_factor_oos,
                        "max_allowed_gap": self.MAX_IS_OOS_PF_GAP,
                    },
                )
            )

        if (
            data.profit_factor_is is not None
            and data.profit_factor_is > self.SUSPICIOUS_PROFIT_FACTOR
        ):
            findings.append(
                ResearchFinding(
                    code="SUSPICIOUS_HIGH_PF",
                    severity=ResearchFindingSeverity.WARNING,
                    component="overfitting",
                    message="El Profit Factor es inusualmente alto y puede indicar sobreoptimización.",
                    evidence={
                        "profit_factor_is": data.profit_factor_is,
                        "suspicious_threshold": self.SUSPICIOUS_PROFIT_FACTOR,
                    },
                )
            )

        if not data.has_real_ticks:
            findings.append(
                ResearchFinding(
                    code="NO_REAL_TICKS",
                    severity=ResearchFindingSeverity.WARNING,
                    component="data_quality",
                    message="El backtest no declara uso de ticks reales.",
                    evidence={"has_real_ticks": data.has_real_ticks},
                )
            )

        missing_costs = []
        if not data.includes_spread:
            missing_costs.append("spread")
        if not data.includes_commissions:
            missing_costs.append("commissions")
        if not data.includes_slippage:
            missing_costs.append("slippage")

        if missing_costs:
            findings.append(
                ResearchFinding(
                    code="MISSING_EXECUTION_COSTS",
                    severity=ResearchFindingSeverity.WARNING,
                    component="execution_costs",
                    message="El backtest no declara todos los costes operativos relevantes.",
                    evidence={"missing_costs": missing_costs},
                )
            )

        return findings