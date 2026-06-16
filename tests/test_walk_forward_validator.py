from core.research.research_models import ResearchValidationInput
from core.research.walk_forward_validator import WalkForwardValidator


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
        "has_walk_forward": True,
        "walk_forward_windows": 8,
        "walk_forward_passed_windows": 7,
        "walk_forward_success_rate": 87.5,
        "has_real_ticks": True,
        "includes_spread": True,
        "includes_commissions": True,
        "includes_slippage": True,
    }
    data.update(overrides)
    return ResearchValidationInput(**data)


def test_walk_forward_validator_accepts_valid_walk_forward_context():
    validator = WalkForwardValidator()

    findings = validator.analyze(_base_input())

    assert findings == []


def test_detects_missing_walk_forward():
    validator = WalkForwardValidator()

    findings = validator.analyze(_base_input(has_walk_forward=False))

    codes = {finding.code for finding in findings}
    assert "NO_WALK_FORWARD" in codes


def test_detects_insufficient_walk_forward_windows():
    validator = WalkForwardValidator()

    findings = validator.analyze(
        _base_input(
            has_walk_forward=True,
            walk_forward_windows=3,
            walk_forward_success_rate=80.0,
        )
    )

    codes = {finding.code for finding in findings}
    assert "INSUFFICIENT_WALK_FORWARD_WINDOWS" in codes


def test_detects_low_walk_forward_success_rate():
    validator = WalkForwardValidator()

    findings = validator.analyze(
        _base_input(
            has_walk_forward=True,
            walk_forward_windows=8,
            walk_forward_success_rate=40.0,
        )
    )

    codes = {finding.code for finding in findings}
    assert "LOW_WALK_FORWARD_SUCCESS_RATE" in codes