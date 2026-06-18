"""
core/research/research_validator.py
-----------------------------------
Orquestador central de validación cuantitativa de Antigravity 2.0.

Integra validadores independientes y resuelve el estado final
de investigación usando exclusivamente los valores del enum ResearchStatus:
  REJECTED, FRAGILE, NEEDS_REVIEW, PROMISING, RESEARCH_APPROVED, PAPER_TRADING_READY

No ejecuta operaciones.
No aprueba operativa real.
No sustituye al RiskEngine.
"""

from __future__ import annotations

from core.research.base_research_validator import BaseResearchValidator
from core.research.overfitting_detector import OverfittingDetector
from core.research.regime_performance_analyzer import RegimePerformanceAnalyzer
from core.research.research_models import (
    ResearchFinding,
    ResearchFindingSeverity,
    ResearchStatus,
    ResearchValidationInput,
    ResearchValidationResult,
)


class ResearchValidator(BaseResearchValidator):
    """
    Orquestador central de validación cuantitativa.

    Integra validaciones independientes:
    - OverfittingDetector
    - RegimePerformanceAnalyzer
    - Comprobaciones propias del orquestador (walk-forward, etc.)

    Criterio de resolución de estado:
    - Algún finding CRITICAL  → REJECTED
    - Algún finding WARNING   → NEEDS_REVIEW
    - Sin findings relevantes → RESEARCH_APPROVED
    """

    def __init__(self) -> None:
        self.overfitting_detector = OverfittingDetector()
        self.regime_performance_analyzer = RegimePerformanceAnalyzer()

    # ── Contrato BaseResearchValidator ───────────────────────────────

    def analyze(
        self,
        data: ResearchValidationInput,
    ) -> list[ResearchFinding]:
        """
        Recopila hallazgos de todos los sub-validadores
        y añade las comprobaciones propias del orquestador.

        Devuelve solo los findings accionables (CRITICAL / WARNING).
        Los findings INFO se descartan a nivel de orquestación.
        """
        findings: list[ResearchFinding] = []

        # ── Sub-validadores ──────────────────────────────────────────
        findings.extend(self.overfitting_detector.analyze(data))

        # Solo ejecutar el analizador de regímenes si hay datos de régimen
        # declarados en metadata.  Si no existen, no es un problema
        # accionable: simplemente no hay datos que analizar.
        if data.metadata.get(RegimePerformanceAnalyzer.METADATA_KEY):
            findings.extend(self.regime_performance_analyzer.analyze(data))

        # ── Comprobaciones propias del orquestador ───────────────────
        if not data.has_walk_forward:
            findings.append(
                ResearchFinding(
                    code="NO_WALK_FORWARD",
                    severity=ResearchFindingSeverity.WARNING,
                    component="orchestrator",
                    message="La estrategia no incluye validación Walk-Forward.",
                    evidence={"has_walk_forward": data.has_walk_forward},
                )
            )

        # Filtrar: solo devolver findings accionables (CRITICAL / WARNING)
        return [
            f
            for f in findings
            if f.severity in (
                ResearchFindingSeverity.CRITICAL,
                ResearchFindingSeverity.WARNING,
            )
        ]

    # ── Orquestación pública ────────────────────────────────────────

    def validate(
        self,
        validation_input: ResearchValidationInput,
    ) -> ResearchValidationResult:
        """
        Punto de entrada principal.  Delega en analyze() y construye
        el ResearchValidationResult con el estado resuelto.
        """
        findings = self.analyze(validation_input)
        status = self._resolve_status(findings)

        return ResearchValidationResult(
            strategy_id=validation_input.strategy_id,
            status=status,
            findings=findings,
            research_score=self._compute_score(findings),
            eligible_for_paper_trading=(status == ResearchStatus.PAPER_TRADING_READY),
            approved_for_real=False,
        )

    # ── Resolución de estado ────────────────────────────────────────

    @staticmethod
    def _resolve_status(
        findings: list[ResearchFinding],
    ) -> ResearchStatus:
        """
        Mapeo explícito de severidades a estados del enum ResearchStatus.

        - CRITICAL  → REJECTED
        - WARNING   → NEEDS_REVIEW
        - Sin findings accionables → RESEARCH_APPROVED
        """
        has_critical = any(
            f.severity == ResearchFindingSeverity.CRITICAL for f in findings
        )
        has_warning = any(
            f.severity == ResearchFindingSeverity.WARNING for f in findings
        )

        if has_critical:
            return ResearchStatus.REJECTED

        if has_warning:
            return ResearchStatus.NEEDS_REVIEW

        return ResearchStatus.RESEARCH_APPROVED

    # ── Score heurístico ────────────────────────────────────────────

    @staticmethod
    def _compute_score(findings: list[ResearchFinding]) -> float:
        """
        Score de 0-100 basado en la cantidad y severidad de findings.
        100 = sin problemas, cada WARNING resta 10, cada CRITICAL resta 25.
        """
        score = 100.0
        for f in findings:
            if f.severity == ResearchFindingSeverity.CRITICAL:
                score -= 25.0
            elif f.severity == ResearchFindingSeverity.WARNING:
                score -= 10.0
        return max(score, 0.0)