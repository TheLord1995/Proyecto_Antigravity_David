from core.research.base_research_validator import BaseResearchValidator
from core.research.research_models import (
    ResearchFinding,
    ResearchFindingSeverity,
    ResearchValidationInput,
)


class WalkForwardValidator(BaseResearchValidator):
    MIN_WINDOWS = 5
    MIN_SUCCESS_RATE = 60.0

    def analyze(self, data: ResearchValidationInput) -> list[ResearchFinding]:
        findings: list[ResearchFinding] = []

        if not data.has_walk_forward:
            findings.append(
                ResearchFinding(
                    code="NO_WALK_FORWARD",
                    severity=ResearchFindingSeverity.WARNING,
                    component="walk_forward",
                    message="La estrategia no incluye validación Walk-Forward.",
                    evidence={"has_walk_forward": data.has_walk_forward},
                )
            )
            return findings

        if data.walk_forward_windows < self.MIN_WINDOWS:
            findings.append(
                ResearchFinding(
                    code="INSUFFICIENT_WALK_FORWARD_WINDOWS",
                    severity=ResearchFindingSeverity.WARNING,
                    component="walk_forward",
                    message="El número de ventanas Walk-Forward es insuficiente.",
                    evidence={
                        "walk_forward_windows": data.walk_forward_windows,
                        "minimum_required": self.MIN_WINDOWS,
                    },
                )
            )

        if (
            data.walk_forward_success_rate is not None
            and data.walk_forward_success_rate < self.MIN_SUCCESS_RATE
        ):
            findings.append(
                ResearchFinding(
                    code="LOW_WALK_FORWARD_SUCCESS_RATE",
                    severity=ResearchFindingSeverity.WARNING,
                    component="walk_forward",
                    message="La tasa de éxito Walk-Forward es inferior al mínimo requerido.",
                    evidence={
                        "walk_forward_success_rate": data.walk_forward_success_rate,
                        "minimum_required": self.MIN_SUCCESS_RATE,
                    },
                )
            )

        return findings