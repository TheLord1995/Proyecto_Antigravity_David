"""
core/ai_validator.py
--------------------
Contratos e interfaces de validadores IA — Fase 4.4.

Implementa la arquitectura por adaptadores para el AI Validator:
- AIValidatorAdapter (Interfaz abstracta)
- MockAIValidator (Implementación concreta offline)

REGLAS DE SEGURIDAD INVARIANTES:
- El AI Validator NO decide operaciones.
- El AI Validator NO ejecuta operaciones.
- El AI Validator NO sustituye al RiskEngine.
- approved_for_real = False SIEMPRE e INMUTABLE.
- Ningún adaptador puede devolver approved_for_real=True.
"""

from abc import ABC, abstractmethod
from datetime import datetime, timezone
import random

from core.ai_models import (
    AIValidatorInput,
    AIValidatorResult,
    AIValidatorVerdict,
    AIRecommendedAction,
)


class AIValidatorAdapter(ABC):
    """
    Clase base abstracta para todos los adaptadores de validación de IA.
    Garantiza que cualquier implementación futura (Remota, OpenRouter, Local, etc.)
    respete las firmas y contratos Pydantic, manteniendo el aislamiento de la lógica.
    """

    @abstractmethod
    def validate_signal(self, input_data: AIValidatorInput) -> AIValidatorResult:
        """
        Evalúa el contexto técnico de una señal de trading.

        :param input_data: Datos de entrada estructurados (AIValidatorInput).
        :return: Resultado de validación estructurado (AIValidatorResult).
                 Siempre con approved_for_real=False.
        """
        pass


class MockAIValidator(AIValidatorAdapter):
    """
    Implementación offline del AI Validator para pruebas unitarias y desarrollo local.
    No requiere conexión de red ni APIs externas.
    Respeta íntegramente las invariantes del proyecto.
    """

    def __init__(self, provider_name: str = "MockAIValidator"):
        self.provider_name = provider_name

    def validate_signal(self, input_data: AIValidatorInput) -> AIValidatorResult:
        """
        Simula la validación de la señal basándose en reglas estáticas sobre el texto
        de la justificación técnica (`technical_reason`) o los parámetros de entrada.
        """
        
        # 1. Regla de "Missing Information"
        if not input_data.technical_reason or len(input_data.technical_reason) < 20:
            return AIValidatorResult(
                signal_id=input_data.signal_id,
                verdict=AIValidatorVerdict.MISSING_INFORMATION,
                confidence=0.0,
                reasons=["Justificación técnica insuficiente o ausente."],
                missing_information=["Falta detalle en technical_reason."],
                recommended_action=AIRecommendedAction.REQUEST_MORE_INFORMATION,
                requires_human_review=True,
                provider=self.provider_name,
                model_name="offline-mock",
                validation_timestamp=datetime.now(timezone.utc),
                approved_for_real=False
            )

        # 2. Regla de política bloqueada (por ejemplo, estrategia rechazada)
        if input_data.strategy_classification == "REJECTED":
            return AIValidatorResult(
                signal_id=input_data.signal_id,
                verdict=AIValidatorVerdict.BLOCKED_BY_POLICY,
                confidence=1.0,
                reasons=["La estrategia de origen está marcada como REJECTED."],
                recommended_action=AIRecommendedAction.BLOCK_SIGNAL,
                requires_human_review=True,
                provider=self.provider_name,
                model_name="offline-mock",
                validation_timestamp=datetime.now(timezone.utc),
                approved_for_real=False
            )

        # 3. Detección simple de contradicciones simuladas
        text_lower = input_data.technical_reason.lower()
        if input_data.direction.upper() == "BUY" and ("bajista" in text_lower or "bearish" in text_lower or "caída" in text_lower):
            return AIValidatorResult(
                signal_id=input_data.signal_id,
                verdict=AIValidatorVerdict.CONTRADICTORY_CONTEXT,
                confidence=0.9,
                reasons=["La dirección BUY contradice explícitamente los términos bajistas en la justificación."],
                contradictions=["Señal de compra con contexto descrito como bajista."],
                recommended_action=AIRecommendedAction.REQUIRE_HUMAN_REVIEW,
                requires_human_review=True,
                provider=self.provider_name,
                model_name="offline-mock",
                validation_timestamp=datetime.now(timezone.utc),
                approved_for_real=False
            )
            
        if input_data.direction.upper() == "SELL" and ("alcista" in text_lower or "bullish" in text_lower or "subida" in text_lower):
            return AIValidatorResult(
                signal_id=input_data.signal_id,
                verdict=AIValidatorVerdict.CONTRADICTORY_CONTEXT,
                confidence=0.9,
                reasons=["La dirección SELL contradice explícitamente los términos alcistas en la justificación."],
                contradictions=["Señal de venta con contexto descrito como alcista."],
                recommended_action=AIRecommendedAction.REQUIRE_HUMAN_REVIEW,
                requires_human_review=True,
                provider=self.provider_name,
                model_name="offline-mock",
                validation_timestamp=datetime.now(timezone.utc),
                approved_for_real=False
            )

        # 4. Contexto Débil (si no hay suficientes indicadores mencionados)
        keywords = ["soporte", "resistencia", "volumen", "rsi", "macd", "ema", "divergencia", "tendencia"]
        found_keywords = sum(1 for kw in keywords if kw in text_lower)
        
        if found_keywords < 2:
            return AIValidatorResult(
                signal_id=input_data.signal_id,
                verdict=AIValidatorVerdict.WEAK_CONTEXT,
                confidence=0.65,
                reasons=["El análisis menciona muy pocos conceptos técnicos claros, contexto superficial."],
                risk_notes=["Análisis técnico poco detallado."],
                recommended_action=AIRecommendedAction.REQUIRE_HUMAN_REVIEW,
                requires_human_review=True,
                provider=self.provider_name,
                model_name="offline-mock",
                validation_timestamp=datetime.now(timezone.utc),
                approved_for_real=False
            )

        # 5. Default a VALID_CONTEXT si pasa los filtros
        return AIValidatorResult(
            signal_id=input_data.signal_id,
            verdict=AIValidatorVerdict.VALID_CONTEXT,
            confidence=0.85,
            reasons=["El contexto técnico declarado parece razonable y alineado con la dirección propuesta."],
            recommended_action=AIRecommendedAction.CONTINUE_TO_RISK_ENGINE,
            requires_human_review=False,
            provider=self.provider_name,
            model_name="offline-mock",
            validation_timestamp=datetime.now(timezone.utc),
            approved_for_real=False
        )
