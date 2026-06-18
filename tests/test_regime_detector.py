"""
tests/test_regime_detector.py
-----------------------------
Tests del RegimeDetector de la capa Research.
"""

from core.research.regime_detector import RegimeDetector
from core.research.research_models import (
    ResearchFindingSeverity,
    ResearchValidationInput,
)


def build_input(tested_regimes: list[str]) -> ResearchValidationInput:
    return ResearchValidationInput(
        strategy_id="ORB_TEST_STRATEGY",
        report_hash_sha256="a" * 64,
        symbol="EURUSD",
        timeframe="H1",
        total_trades=150,
        profit_factor_is=1.60,
        profit_factor_oos=1.35,
        max_drawdown_pct=12.5,
        sharpe_ratio=1.20,
        expectancy=0.15,
        has_in_sample=True,
        has_out_of_sample=True,
        has_walk_forward=True,
        walk_forward_windows=6,
        walk_forward_passed_windows=5,
        walk_forward_success_rate=83.33,
        has_real_ticks=True,
        includes_spread=True,
        includes_commissions=True,
        includes_slippage=True,
        tested_assets=["EURUSD", "GBPUSD"],
        tested_regimes=tested_regimes,
        metadata={"source": "unit_test"},
    )


def test_regime_detector_rejects_when_no_regimes_declared():
    detector = RegimeDetector()
    data = build_input(tested_regimes=[])

    findings = detector.analyze(data)

    assert len(findings) == 1
    assert findings[0].code == "NO_REGIME_VALIDATION"
    assert findings[0].severity == ResearchFindingSeverity.CRITICAL
    assert findings[0].component == "regime"


def test_regime_detector_warns_when_only_one_regime_declared():
    detector = RegimeDetector()
    data = build_input(tested_regimes=["TRENDING_BULLISH"])

    findings = detector.analyze(data)

    assert len(findings) == 1
    assert findings[0].code == "REGIME_COVERAGE_LOW"
    assert findings[0].severity == ResearchFindingSeverity.WARNING
    assert findings[0].component == "regime"


def test_regime_detector_warns_when_coverage_is_partial():
    detector = RegimeDetector()
    data = build_input(
        tested_regimes=[
            "TRENDING_BULLISH",
            "RANGING",
        ]
    )

    findings = detector.analyze(data)

    assert len(findings) == 1
    assert findings[0].code == "REGIME_COVERAGE_PARTIAL"
    assert findings[0].severity == ResearchFindingSeverity.WARNING
    assert findings[0].component == "regime"


def test_regime_detector_returns_info_when_required_regimes_are_covered():
    detector = RegimeDetector()
    data = build_input(
        tested_regimes=[
            "TRENDING_BULLISH",
            "TRENDING_BEARISH",
            "RANGING",
        ]
    )

    findings = detector.analyze(data)

    assert len(findings) == 1
    assert findings[0].code == "REGIME_COVERAGE_OK"
    assert findings[0].severity == ResearchFindingSeverity.INFO
    assert findings[0].component == "regime"


def test_regime_detector_normalizes_lowercase_regimes():
    detector = RegimeDetector()
    data = build_input(
        tested_regimes=[
            "trending_bullish",
            "trending_bearish",
            "ranging",
        ]
    )

    findings = detector.analyze(data)

    assert len(findings) == 1
    assert findings[0].code == "REGIME_COVERAGE_OK"
    assert findings[0].severity == ResearchFindingSeverity.INFO