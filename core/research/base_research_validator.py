"""
core/research/base_research_validator.py
----------------------------------------
Contrato base para validadores de investigación cuantitativa.

Ningún validador de esta capa ejecuta operaciones, aprueba operativa real
ni sustituye al RiskEngine.
"""

from abc import ABC, abstractmethod

from core.research.research_models import ResearchFinding, ResearchValidationInput


class BaseResearchValidator(ABC):
    """Interfaz común para validadores de la capa research."""

    @abstractmethod
    def analyze(self, data: ResearchValidationInput) -> list[ResearchFinding]:
        """Analiza una estrategia/backtest y devuelve hallazgos de investigación."""
        raise NotImplementedError