"""
core/research/research_validator.py
-----------------------------------
Orquestador de la capa de investigación cuantitativa.

No ejecuta operaciones.
No aprueba operativa real.
No sustituye al RiskEngine.
"""

from core.research.overfitting_detector import OverfittingDetector
from core.research.regime_detector import RegimeDetector
from core.research.research_models import (
    ResearchFindingSeverity,
    ResearchStatus,
    ResearchValidationInput,
    ResearchValidationResult,
)
from core.research.stress_tester import StressTester
from core.research.walk_forward_validator import WalkForwardValidator


class ResearchValidator:
    """Orquesta validadores de investigación cuantitativa."""

    def __init__(self):
        self.overfitting_detector = OverfittingDetector()
        self.walk_forward_validator = WalkForwardValidator()
        self.regime_detector = RegimeDetector()
        self.stress_tester = StressTester()

    def validate(self, data: ResearchValidationInput) -> ResearchValidationResult:
        findings = []

        findings.extend(
            self.overfitting_detector.analyze(data)
        )

        findings.extend(
            self.walk_forward_validator.analyze(data)
        )

        if data.tested_regimes:
            regime_findings = self.regime_detector.analyze(data)
            findings.extend(
                finding
                for finding in regime_findings
                if finding.severity != ResearchFindingSeverity.INFO
            )

        stress_findings = self.stress_tester.analyze(data)
        findings.extend(
            finding
            for finding in stress_findings
            if finding.severity != ResearchFindingSeverity.INFO
        )

        severities = {finding.severity for finding in findings}

        if ResearchFindingSeverity.CRITICAL in severities:
            status = ResearchStatus.REJECTED
            score = 0
        elif ResearchFindingSeverity.WARNING in severities:
            status = ResearchStatus.NEEDS_REVIEW
            score = 60
        else:
            status = ResearchStatus.RESEARCH_APPROVED
            score = 85

        return ResearchValidationResult(
            strategy_id=data.strategy_id,
            status=status,
            findings=findings,
            research_score=score,
            eligible_for_paper_trading=False,
            approved_for_real=False,
        )