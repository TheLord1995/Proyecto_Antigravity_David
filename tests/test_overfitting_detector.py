from core.research.overfitting_detector import OverfittingDetector
from core.research.research_models import ResearchValidationInput


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


def test_overfitting_detector_returns_no_findings_for_clean_input():
    detector = OverfittingDetector()
    findings = detector.analyze(_base_input())

    assert findings == []


def test_detects_missing_out_of_sample():
    detector = OverfittingDetector()
    findings = detector.analyze(_base_input(has_out_of_sample=False))

    codes = {finding.code for finding in findings}
    assert "NO_OOS" in codes


def test_detects_low_trade_count():
    detector = OverfittingDetector()
    findings = detector.analyze(_base_input(total_trades=50))

    codes = {finding.code for finding in findings}
    assert "LOW_TRADE_COUNT" in codes


def test_detects_large_is_oos_profit_factor_gap():
    detector = OverfittingDetector()
    findings = detector.analyze(
        _base_input(profit_factor_is=2.0, profit_factor_oos=1.2)
    )

    codes = {finding.code for finding in findings}
    assert "IS_OOS_PF_GAP" in codes


def test_detects_suspicious_high_profit_factor():
    detector = OverfittingDetector()
    findings = detector.analyze(_base_input(profit_factor_is=3.0))

    codes = {finding.code for finding in findings}
    assert "SUSPICIOUS_HIGH_PF" in codes


def test_detects_missing_real_ticks():
    detector = OverfittingDetector()
    findings = detector.analyze(_base_input(has_real_ticks=False))

    codes = {finding.code for finding in findings}
    assert "NO_REAL_TICKS" in codes


def test_detects_missing_execution_costs():
    detector = OverfittingDetector()
    findings = detector.analyze(
        _base_input(
            includes_spread=False,
            includes_commissions=True,
            includes_slippage=False,
        )
    )

    codes = {finding.code for finding in findings}
    assert "MISSING_EXECUTION_COSTS" in codes