"""
core/research/regime_detector.py
---------------------------------
Validador determinista de cobertura de regímenes de mercado.

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


class RegimeDetector(BaseResearchValidator):
    """Evalúa si una estrategia ha sido probada en suficientes regímenes de mercado."""

    REQUIRED_REGIMES = {
        "TRENDING_BULLISH",
        "TRENDING_BEARISH",
        "RANGING",
    }

    MIN_ACCEPTABLE_REGIMES = 2

    def analyze(self, data: ResearchValidationInput) -> list[ResearchFinding]:
        findings: list[ResearchFinding] = []

        tested_regimes = {regime.upper() for regime in data.tested_regimes}
        covered_required_regimes = tested_regimes.intersection(self.REQUIRED_REGIMES)
        missing_required_regimes = self.REQUIRED_REGIMES.difference(tested_regimes)

        if not tested_regimes:
            findings.append(
                ResearchFinding(
                    code="NO_REGIME_VALIDATION",
                    severity=ResearchFindingSeverity.CRITICAL,
                    component="regime",
                    message="La estrategia no declara validación en ningún régimen de mercado.",
                    evidence={
                        "tested_regimes": data.tested_regimes,
                        "required_regimes": sorted(self.REQUIRED_REGIMES),
                    },
                )
            )
            return findings

        if len(covered_required_regimes) < self.MIN_ACCEPTABLE_REGIMES:
            findings.append(
                ResearchFinding(
                    code="REGIME_COVERAGE_LOW",
                    severity=ResearchFindingSeverity.WARNING,
                    component="regime",
                    message="La estrategia ha sido probada en pocos regímenes de mercado.",
                    evidence={
                        "tested_regimes": sorted(tested_regimes),
                        "covered_required_regimes": sorted(covered_required_regimes),
                        "missing_required_regimes": sorted(missing_required_regimes),
                        "minimum_acceptable_regimes": self.MIN_ACCEPTABLE_REGIMES,
                    },
                )
            )
            return findings

        if missing_required_regimes:
            findings.append(
                ResearchFinding(
                    code="REGIME_COVERAGE_PARTIAL",
                    severity=ResearchFindingSeverity.WARNING,
                    component="regime",
                    message="La estrategia no cubre todos los regímenes de mercado recomendados.",
                    evidence={
                        "tested_regimes": sorted(tested_regimes),
                        "covered_required_regimes": sorted(covered_required_regimes),
                        "missing_required_regimes": sorted(missing_required_regimes),
                    },
                )
            )
            return findings

        findings.append(
            ResearchFinding(
                code="REGIME_COVERAGE_OK",
                severity=ResearchFindingSeverity.INFO,
                component="regime",
                message="La estrategia declara validación suficiente en distintos regímenes de mercado.",
                evidence={
                    "tested_regimes": sorted(tested_regimes),
                    "covered_required_regimes": sorted(covered_required_regimes),
                },
            )
        )

        return findings