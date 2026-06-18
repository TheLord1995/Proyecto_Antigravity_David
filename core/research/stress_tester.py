"""
core/research/stress_tester.py
------------------------------
Validador determinista de estrés para estrategias cuantitativas.

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


class StressTester(BaseResearchValidator):
    """Evalúa señales básicas de fragilidad bajo condiciones adversas."""

    MAX_DRAWDOWN_WARNING_PCT = 25.0
    MAX_DRAWDOWN_CRITICAL_PCT = 40.0
    MIN_EXPECTANCY = 0.0
    MIN_SHARPE_WARNING = 0.50
    MIN_PROFIT_FACTOR_OOS_WARNING = 1.10

    def analyze(self, data: ResearchValidationInput) -> list[ResearchFinding]:
        findings: list[ResearchFinding] = []

        if (
            data.max_drawdown_pct is not None
            and data.max_drawdown_pct >= self.MAX_DRAWDOWN_CRITICAL_PCT
        ):
            findings.append(
                ResearchFinding(
                    code="STRESS_DRAWDOWN_CRITICAL",
                    severity=ResearchFindingSeverity.CRITICAL,
                    component="stress",
                    message="El drawdown máximo es crítico para una estrategia candidata a validación investigadora.",
                    evidence={
                        "max_drawdown_pct": data.max_drawdown_pct,
                        "critical_threshold_pct": self.MAX_DRAWDOWN_CRITICAL_PCT,
                    },
                )
            )

        elif (
            data.max_drawdown_pct is not None
            and data.max_drawdown_pct >= self.MAX_DRAWDOWN_WARNING_PCT
        ):
            findings.append(
                ResearchFinding(
                    code="STRESS_DRAWDOWN_HIGH",
                    severity=ResearchFindingSeverity.WARNING,
                    component="stress",
                    message="El drawdown máximo es elevado y requiere revisión antes de paper trading.",
                    evidence={
                        "max_drawdown_pct": data.max_drawdown_pct,
                        "warning_threshold_pct": self.MAX_DRAWDOWN_WARNING_PCT,
                    },
                )
            )

        if data.expectancy is not None and data.expectancy <= self.MIN_EXPECTANCY:
            findings.append(
                ResearchFinding(
                    code="STRESS_EXPECTANCY_NON_POSITIVE",
                    severity=ResearchFindingSeverity.CRITICAL,
                    component="stress",
                    message="La esperanza matemática no es positiva bajo las métricas declaradas.",
                    evidence={
                        "expectancy": data.expectancy,
                        "minimum_required": self.MIN_EXPECTANCY,
                    },
                )
            )

        if (
            data.sharpe_ratio is not None
            and data.sharpe_ratio < self.MIN_SHARPE_WARNING
        ):
            findings.append(
                ResearchFinding(
                    code="STRESS_LOW_SHARPE",
                    severity=ResearchFindingSeverity.WARNING,
                    component="stress",
                    message="El Sharpe Ratio es bajo y puede indicar rentabilidad insuficiente ajustada al riesgo.",
                    evidence={
                        "sharpe_ratio": data.sharpe_ratio,
                        "minimum_warning_threshold": self.MIN_SHARPE_WARNING,
                    },
                )
            )

        if (
            data.profit_factor_oos is not None
            and data.profit_factor_oos < self.MIN_PROFIT_FACTOR_OOS_WARNING
        ):
            findings.append(
                ResearchFinding(
                    code="STRESS_LOW_OOS_PROFIT_FACTOR",
                    severity=ResearchFindingSeverity.WARNING,
                    component="stress",
                    message="El Profit Factor Out of Sample es bajo bajo criterios de estrés.",
                    evidence={
                        "profit_factor_oos": data.profit_factor_oos,
                        "minimum_warning_threshold": self.MIN_PROFIT_FACTOR_OOS_WARNING,
                    },
                )
            )

        if not findings:
            findings.append(
                ResearchFinding(
                    code="STRESS_CHECK_OK",
                    severity=ResearchFindingSeverity.INFO,
                    component="stress",
                    message="La estrategia no presenta señales básicas de fragilidad en la prueba de estrés.",
                    evidence={
                        "max_drawdown_pct": data.max_drawdown_pct,
                        "expectancy": data.expectancy,
                        "sharpe_ratio": data.sharpe_ratio,
                        "profit_factor_oos": data.profit_factor_oos,
                    },
                )
            )

        return findings