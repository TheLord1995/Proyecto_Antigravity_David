"""
tests/test_ai_validator_adapters.py
-----------------------------------
Pruebas unitarias para MockAIValidator y la interfaz de adaptadores.
Verifica que las invariantes de seguridad y los contratos de Fase 4.4 se cumplen en la implementación.
"""

import pytest
from core.ai_models import (
    AIValidatorInput,
    AIValidatorVerdict,
    AIRecommendedAction,
)
from core.ai_validator import MockAIValidator

@pytest.fixture
def mock_validator():
    return MockAIValidator()

def make_test_input(**overrides):
    base = {
        "signal_id": "TEST-123",
        "symbol": "EURUSD",
        "direction": "BUY",
        "timeframe": "H1",
        "technical_reason": "El precio muestra soporte claro con fuerte volumen alcista, cruce dorado en MACD y RSI saliendo de sobreventa."
    }
    base.update(overrides)
    return AIValidatorInput(**base)

def test_mock_validator_valid_context(mock_validator):
    """Prueba un contexto ideal que debe devolver VALID_CONTEXT"""
    input_data = make_test_input()
    result = mock_validator.validate_signal(input_data)
    
    assert result.verdict == AIValidatorVerdict.VALID_CONTEXT
    assert result.recommended_action == AIRecommendedAction.CONTINUE_TO_RISK_ENGINE
    assert result.requires_human_review is False
    assert result.approved_for_real is False
    assert result.provider == "MockAIValidator"

def test_mock_validator_blocked_by_policy(mock_validator):
    """Prueba que si la estrategia está REJECTED, el validador bloquea inmediatamente"""
    input_data = make_test_input(strategy_classification="REJECTED")
    result = mock_validator.validate_signal(input_data)
    
    assert result.verdict == AIValidatorVerdict.BLOCKED_BY_POLICY
    assert result.recommended_action == AIRecommendedAction.BLOCK_SIGNAL
    assert result.requires_human_review is True
    assert result.approved_for_real is False

def test_mock_validator_contradictory_context_buy(mock_validator):
    """Prueba contradicción: Dirección BUY pero texto describe tendencia bajista"""
    input_data = make_test_input(
        direction="BUY",
        technical_reason="El precio rompe el soporte H4. Fuerte tendencia bajista detectada con velas de gran cuerpo."
    )
    result = mock_validator.validate_signal(input_data)
    
    assert result.verdict == AIValidatorVerdict.CONTRADICTORY_CONTEXT
    assert result.recommended_action == AIRecommendedAction.REQUIRE_HUMAN_REVIEW
    assert result.requires_human_review is True
    assert result.approved_for_real is False
    assert len(result.contradictions) > 0

def test_mock_validator_contradictory_context_sell(mock_validator):
    """Prueba contradicción: Dirección SELL pero texto describe tendencia alcista"""
    input_data = make_test_input(
        direction="SELL",
        technical_reason="Fuerte ruptura de resistencia H1. Se espera una subida masiva. Divergencia alcista clara."
    )
    result = mock_validator.validate_signal(input_data)
    
    assert result.verdict == AIValidatorVerdict.CONTRADICTORY_CONTEXT
    assert result.recommended_action == AIRecommendedAction.REQUIRE_HUMAN_REVIEW
    assert result.requires_human_review is True
    assert result.approved_for_real is False
    assert len(result.contradictions) > 0

def test_mock_validator_weak_context(mock_validator):
    """Prueba que si no hay suficientes conceptos técnicos, se marca como WEAK_CONTEXT"""
    input_data = make_test_input(
        technical_reason="El precio se ve bien. Creo que va a subir hoy. Buena suerte a todos."
    )
    result = mock_validator.validate_signal(input_data)
    
    assert result.verdict == AIValidatorVerdict.WEAK_CONTEXT
    assert result.recommended_action == AIRecommendedAction.REQUIRE_HUMAN_REVIEW
    assert result.requires_human_review is True
    assert result.approved_for_real is False

def test_approved_for_real_is_never_true(mock_validator):
    """
    Test supremo de seguridad.
    Verifica que approved_for_real NUNCA puede ser True independientemente de lo que se le pase.
    """
    inputs = [
        make_test_input(),
        make_test_input(strategy_classification="REJECTED"),
        make_test_input(direction="SELL", technical_reason="Tendencia alcista clara y soporte fuerte. Divergencia de volumen."),
        make_test_input(technical_reason="Short reason this time but still valid."),
    ]
    
    for data in inputs:
        result = mock_validator.validate_signal(data)
        assert result.approved_for_real is False, f"INVARIANTE DE SEGURIDAD VIOLADA: approved_for_real es True para {data}"
