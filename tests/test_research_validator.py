"""
tests/test_research_validator.py
---------------------------------
Tests del ResearchValidator (orquestador central).

Valida integración de los 5 sub-validadores:
- OverfittingDetector
- WalkForwardValidator
- RegimeDetector
- RegimePerformanceAnalyzer
- StressTester
"""

from core.research.research_models import (
    ResearchStatus,
    ResearchValidationInput,
)
from core.research.research_validator import ResearchValidator


def _base_input(**overrides):
    """Construye un input de estrategia limpia que pasa TODOS los validadores."""
    data = {
        "strategy_id": "ORB_EURUSD_H1",
        "report_hash_sha256": "a" * 64,
        "symbol": "EURUSD",
        "timeframe": "H1",
        "total_trades": 250,
        "profit_factor_is": 1.6,
        "profit_factor_oos": 1.4,
        "max_drawdown_pct": 12.5,
        "sharpe_ratio": 1.20,
        "expectancy": 0.15,
        "has_in_sample": True,
        "has_out_of_sample": True,
        "has_walk_forward": True,
        "walk_forward_windows": 8,
        "walk_forward_passed_windows": 7,
        "walk_forward_success_rate": 87.5,
        "has_real_ticks": True,
        "includes_spread": True,
        "includes_commissions": True,
        "includes_slippage": True,
        "tested_regimes": [
            "TRENDING_BULLISH",
            "TRENDING_BEARISH",
            "RANGING",
        ],
    }
    data.update(overrides)
    return ResearchValidationInput(**data)


def test_clean_strategy_is_research_approved():
    validator = ResearchValidator()

    result = validator.validate(_base_input())

    assert result.status == ResearchStatus.RESEARCH_APPROVED
    assert len(result.findings) == 0
    assert result.approved_for_real is False


def test_missing_oos_is_rejected():
    validator = ResearchValidator()

    result = validator.validate(
        _base_input(has_out_of_sample=False)
    )

    assert result.status == ResearchStatus.REJECTED


def test_warning_strategy_needs_review():
    validator = ResearchValidator()

    result = validator.validate(
        _base_input(total_trades=50)
    )

    assert result.status == ResearchStatus.NEEDS_REVIEW


def test_missing_walk_forward_requires_review():
    validator = ResearchValidator()

    result = validator.validate(
        _base_input(has_walk_forward=False)
    )

    assert result.status == ResearchStatus.NEEDS_REVIEW


def test_real_execution_always_false():
    validator = ResearchValidator()

    result = validator.validate(_base_input())

    assert result.approved_for_real is False


# ── Tests de integración de StressTester ─────────────────────────


def test_critical_drawdown_is_rejected_via_stress_tester():
    """Verifica que StressTester integrado rechaza drawdown ≥ 40%."""
    validator = ResearchValidator()

    result = validator.validate(
        _base_input(max_drawdown_pct=45.0)
    )

    assert result.status == ResearchStatus.REJECTED
    codes = {f.code for f in result.findings}
    assert "STRESS_DRAWDOWN_CRITICAL" in codes


def test_non_positive_expectancy_is_rejected_via_stress_tester():
    """Verifica que StressTester integrado rechaza expectancy ≤ 0."""
    validator = ResearchValidator()

    result = validator.validate(
        _base_input(expectancy=0.0)
    )

    assert result.status == ResearchStatus.REJECTED
    codes = {f.code for f in result.findings}
    assert "STRESS_EXPECTANCY_NON_POSITIVE" in codes


# ── Tests de integración de WalkForwardValidator ─────────────────


def test_insufficient_walk_forward_windows_needs_review():
    """Verifica que WalkForwardValidator integrado detecta ventanas insuficientes."""
    validator = ResearchValidator()

    result = validator.validate(
        _base_input(
            has_walk_forward=True,
            walk_forward_windows=3,
            walk_forward_success_rate=80.0,
        )
    )

    assert result.status == ResearchStatus.NEEDS_REVIEW
    codes = {f.code for f in result.findings}
    assert "INSUFFICIENT_WALK_FORWARD_WINDOWS" in codes


def test_low_walk_forward_success_rate_needs_review():
    """Verifica que WalkForwardValidator integrado detecta success rate bajo."""
    validator = ResearchValidator()

    result = validator.validate(
        _base_input(
            has_walk_forward=True,
            walk_forward_windows=8,
            walk_forward_success_rate=40.0,
        )
    )

    assert result.status == ResearchStatus.NEEDS_REVIEW
    codes = {f.code for f in result.findings}
    assert "LOW_WALK_FORWARD_SUCCESS_RATE" in codes


# ── Tests de integración de RegimeDetector ───────────────────────


def test_no_regimes_declared_is_rejected():
    """Verifica que RegimeDetector integrado rechaza sin regímenes declarados."""
    validator = ResearchValidator()

    result = validator.validate(
        _base_input(tested_regimes=[])
    )

    assert result.status == ResearchStatus.REJECTED
    codes = {f.code for f in result.findings}
    assert "NO_REGIME_VALIDATION" in codes


def test_partial_regime_coverage_needs_review():
    """Verifica que RegimeDetector integrado detecta cobertura parcial."""
    validator = ResearchValidator()

    result = validator.validate(
        _base_input(tested_regimes=["TRENDING_BULLISH", "RANGING"])
    )

    assert result.status == ResearchStatus.NEEDS_REVIEW
    codes = {f.code for f in result.findings}
    assert "REGIME_COVERAGE_PARTIAL" in codes