from core.research.research_models import (
    ResearchStatus,
    ResearchValidationInput,
)
from core.research.research_validator import ResearchValidator


def _base_input(**overrides):
    data = {
        "strategy_id": "ORB_EURUSD_H1",
        "report_hash_sha256": "a" * 64,
        "symbol": "EURUSD",
        "timeframe": "H1",
        "total_trades": 250,
        "profit_factor_is": 1.6,
        "profit_factor_oos": 1.4,
        "has_in_sample": True,
        "has_out_of_sample": True,
        "has_real_ticks": True,
        "includes_spread": True,
        "includes_commissions": True,
        "includes_slippage": True,
    }
    data.update(overrides)
    return ResearchValidationInput(**data)


def test_clean_strategy_is_research_approved():
    validator = ResearchValidator()

    result = validator.validate(_base_input())

    assert result.status == ResearchStatus.RESEARCH_APPROVED
    assert len(result.findings) == 0


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


def test_real_execution_always_false():
    validator = ResearchValidator()

    result = validator.validate(_base_input())

    assert result.approved_for_real is False