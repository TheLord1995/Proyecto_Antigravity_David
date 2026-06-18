"""
tests/test_stress_tester.py
---------------------------
Tests del StressTester de la capa Research.
"""

from core.research.research_models import (
    ResearchFindingSeverity,
    ResearchValidationInput,
)
from core.research.stress_tester import StressTester


def build_input(
    max_drawdown_pct: float | None = 12.5,
    expectancy: float | None = 0.15,
    sharpe_ratio: float | None = 1.20,
    profit_factor_oos: float | None = 1.35,
) -> ResearchValidationInput:
    return ResearchValidationInput(
        strategy_id="ORB_TEST_STRATEGY",
        report_hash_sha256="a" * 64,
        symbol="EURUSD",
        timeframe="H1",
        total_trades=150,
        profit_factor_is=1.60,
        profit_factor_oos=profit_factor_oos,
        max_drawdown_pct=max_drawdown_pct,
        sharpe_ratio=sharpe_ratio,
        expectancy=expectancy,
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
        tested_regimes=[
            "TRENDING_BULLISH",
            "TRENDING_BEARISH",
            "RANGING",
        ],
        metadata={"source": "unit_test"},
    )


def test_stress_tester_returns_info_when_metrics_are_healthy():
    tester = StressTester()
    data = build_input()

    findings = tester.analyze(data)

    assert len(findings) == 1
    assert findings[0].code == "STRESS_CHECK_OK"
    assert findings[0].severity == ResearchFindingSeverity.INFO
    assert findings[0].component == "stress"


def test_stress_tester_warns_when_drawdown_is_high():
    tester = StressTester()
    data = build_input(max_drawdown_pct=27.0)

    findings = tester.analyze(data)

    assert any(finding.code == "STRESS_DRAWDOWN_HIGH" for finding in findings)
    assert any(
        finding.severity == ResearchFindingSeverity.WARNING
        for finding in findings
    )


def test_stress_tester_rejects_when_drawdown_is_critical():
    tester = StressTester()
    data = build_input(max_drawdown_pct=42.0)

    findings = tester.analyze(data)

    assert any(finding.code == "STRESS_DRAWDOWN_CRITICAL" for finding in findings)
    assert any(
        finding.severity == ResearchFindingSeverity.CRITICAL
        for finding in findings
    )


def test_stress_tester_rejects_non_positive_expectancy():
    tester = StressTester()
    data = build_input(expectancy=0.0)

    findings = tester.analyze(data)

    assert any(
        finding.code == "STRESS_EXPECTANCY_NON_POSITIVE"
        for finding in findings
    )
    assert any(
        finding.severity == ResearchFindingSeverity.CRITICAL
        for finding in findings
    )


def test_stress_tester_warns_low_sharpe_ratio():
    tester = StressTester()
    data = build_input(sharpe_ratio=0.30)

    findings = tester.analyze(data)

    assert any(finding.code == "STRESS_LOW_SHARPE" for finding in findings)
    assert any(
        finding.severity == ResearchFindingSeverity.WARNING
        for finding in findings
    )


def test_stress_tester_warns_low_oos_profit_factor():
    tester = StressTester()
    data = build_input(profit_factor_oos=1.05)

    findings = tester.analyze(data)

    assert any(
        finding.code == "STRESS_LOW_OOS_PROFIT_FACTOR"
        for finding in findings
    )
    assert any(
        finding.severity == ResearchFindingSeverity.WARNING
        for finding in findings
    )


def test_stress_tester_can_return_multiple_findings():
    tester = StressTester()
    data = build_input(
        max_drawdown_pct=45.0,
        expectancy=-0.10,
        sharpe_ratio=0.20,
        profit_factor_oos=0.95,
    )

    findings = tester.analyze(data)
    codes = {finding.code for finding in findings}

    assert "STRESS_DRAWDOWN_CRITICAL" in codes
    assert "STRESS_EXPECTANCY_NON_POSITIVE" in codes
    assert "STRESS_LOW_SHARPE" in codes
    assert "STRESS_LOW_OOS_PROFIT_FACTOR" in codes