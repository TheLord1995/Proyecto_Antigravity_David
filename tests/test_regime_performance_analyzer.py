"""
tests/test_regime_performance_analyzer.py
-----------------------------------------
Tests del RegimePerformanceAnalyzer de la capa Research.
"""

from core.research.regime_performance_analyzer import RegimePerformanceAnalyzer
from core.research.research_models import (
    ResearchFindingSeverity,
    ResearchValidationInput,
)


def build_input(metadata: dict | None = None) -> ResearchValidationInput:
    return ResearchValidationInput(
        strategy_id="ORB_TEST_STRATEGY",
        report_hash_sha256="a" * 64,
        symbol="EURUSD",
        timeframe="H1",
        total_trades=180,
        profit_factor_is=1.70,
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
        tested_regimes=[
            "TRENDING_BULLISH",
            "TRENDING_BEARISH",
            "RANGING",
        ],
        metadata=metadata or {},
    )


def test_regime_performance_warns_when_no_data_is_declared():
    analyzer = RegimePerformanceAnalyzer()
    data = build_input()

    findings = analyzer.analyze(data)

    assert len(findings) == 1
    assert findings[0].code == "NO_REGIME_PERFORMANCE_DATA"
    assert findings[0].severity == ResearchFindingSeverity.WARNING
    assert findings[0].component == "regime_performance"


def test_regime_performance_rejects_invalid_format():
    analyzer = RegimePerformanceAnalyzer()
    data = build_input(
        metadata={
            "regime_performance": ["invalid", "format"],
        }
    )

    findings = analyzer.analyze(data)

    assert len(findings) == 1
    assert findings[0].code == "INVALID_REGIME_PERFORMANCE_FORMAT"
    assert findings[0].severity == ResearchFindingSeverity.CRITICAL


def test_regime_performance_returns_info_when_all_regimes_are_healthy():
    analyzer = RegimePerformanceAnalyzer()
    data = build_input(
        metadata={
            "regime_performance": {
                "TRENDING_BULLISH": {
                    "trades": 70,
                    "profit_factor": 1.45,
                    "expectancy": 0.18,
                    "max_drawdown_pct": 11.0,
                },
                "TRENDING_BEARISH": {
                    "trades": 55,
                    "profit_factor": 1.30,
                    "expectancy": 0.11,
                    "max_drawdown_pct": 14.5,
                },
                "RANGING": {
                    "trades": 45,
                    "profit_factor": 1.18,
                    "expectancy": 0.06,
                    "max_drawdown_pct": 18.0,
                },
            }
        }
    )

    findings = analyzer.analyze(data)

    assert len(findings) == 1
    assert findings[0].code == "REGIME_PERFORMANCE_OK"
    assert findings[0].severity == ResearchFindingSeverity.INFO


def test_regime_performance_warns_low_trade_count():
    analyzer = RegimePerformanceAnalyzer()
    data = build_input(
        metadata={
            "regime_performance": {
                "RANGING": {
                    "trades": 12,
                    "profit_factor": 1.25,
                    "expectancy": 0.08,
                    "max_drawdown_pct": 12.0,
                }
            }
        }
    )

    findings = analyzer.analyze(data)

    assert any(finding.code == "REGIME_LOW_TRADE_COUNT" for finding in findings)
    assert any(
        finding.severity == ResearchFindingSeverity.WARNING
        for finding in findings
    )


def test_regime_performance_warns_low_profit_factor():
    analyzer = RegimePerformanceAnalyzer()
    data = build_input(
        metadata={
            "regime_performance": {
                "TRENDING_BEARISH": {
                    "trades": 40,
                    "profit_factor": 1.02,
                    "expectancy": 0.05,
                    "max_drawdown_pct": 16.0,
                }
            }
        }
    )

    findings = analyzer.analyze(data)

    assert any(finding.code == "REGIME_LOW_PROFIT_FACTOR" for finding in findings)
    assert any(
        finding.severity == ResearchFindingSeverity.WARNING
        for finding in findings
    )


def test_regime_performance_rejects_non_positive_expectancy():
    analyzer = RegimePerformanceAnalyzer()
    data = build_input(
        metadata={
            "regime_performance": {
                "TRENDING_BULLISH": {
                    "trades": 60,
                    "profit_factor": 1.20,
                    "expectancy": 0.0,
                    "max_drawdown_pct": 10.0,
                }
            }
        }
    )

    findings = analyzer.analyze(data)

    assert any(
        finding.code == "REGIME_NON_POSITIVE_EXPECTANCY"
        for finding in findings
    )
    assert any(
        finding.severity == ResearchFindingSeverity.CRITICAL
        for finding in findings
    )


def test_regime_performance_warns_high_drawdown():
    analyzer = RegimePerformanceAnalyzer()
    data = build_input(
        metadata={
            "regime_performance": {
                "RANGING": {
                    "trades": 50,
                    "profit_factor": 1.20,
                    "expectancy": 0.05,
                    "max_drawdown_pct": 35.0,
                }
            }
        }
    )

    findings = analyzer.analyze(data)

    assert any(finding.code == "REGIME_DRAWDOWN_TOO_HIGH" for finding in findings)
    assert any(
        finding.severity == ResearchFindingSeverity.WARNING
        for finding in findings
    )


def test_regime_performance_can_return_multiple_findings():
    analyzer = RegimePerformanceAnalyzer()
    data = build_input(
        metadata={
            "regime_performance": {
                "TRENDING_BULLISH": {
                    "trades": 10,
                    "profit_factor": 0.95,
                    "expectancy": -0.04,
                    "max_drawdown_pct": 38.0,
                }
            }
        }
    )

    findings = analyzer.analyze(data)
    codes = {finding.code for finding in findings}

    assert "REGIME_LOW_TRADE_COUNT" in codes
    assert "REGIME_LOW_PROFIT_FACTOR" in codes
    assert "REGIME_NON_POSITIVE_EXPECTANCY" in codes
    assert "REGIME_DRAWDOWN_TOO_HIGH" in codes