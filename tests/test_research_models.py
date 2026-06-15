import pytest

from core.research.research_models import (
    ResearchFinding,
    ResearchFindingSeverity,
    ResearchStatus,
    ResearchValidationInput,
    ResearchValidationResult,
)


def test_research_validation_input_accepts_safe_context():
    data = ResearchValidationInput(
        strategy_id="ORB_EURUSD_H1",
        report_hash_sha256="a" * 64,
        symbol="EURUSD",
        timeframe="H1",
        total_trades=250,
        profit_factor_is=1.7,
        profit_factor_oos=1.35,
        max_drawdown_pct=12.5,
        has_in_sample=True,
        has_out_of_sample=True,
        has_walk_forward=False,
        has_real_ticks=True,
        includes_spread=True,
        includes_commissions=True,
        includes_slippage=False,
        tested_assets=["EURUSD", "GBPUSD"],
        tested_regimes=["trend", "range"],
    )

    assert data.strategy_id == "ORB_EURUSD_H1"
    assert data.total_trades == 250
    assert data.has_out_of_sample is True


def test_research_validation_input_rejects_real_execution_metadata():
    with pytest.raises(ValueError):
        ResearchValidationInput(
            strategy_id="unsafe_strategy",
            report_hash_sha256="b" * 64,
            total_trades=100,
            metadata={"approved_for_real": True},
        )


def test_research_validation_result_never_approves_real_execution():
    with pytest.raises(ValueError):
        ResearchValidationResult(
            strategy_id="unsafe_strategy",
            status=ResearchStatus.RESEARCH_APPROVED,
            research_score=85,
            approved_for_real=True,
        )


def test_paper_trading_ready_sets_paper_eligibility():
    result = ResearchValidationResult(
        strategy_id="robust_strategy",
        status=ResearchStatus.PAPER_TRADING_READY,
        research_score=90,
    )

    assert result.eligible_for_paper_trading is True
    assert result.approved_for_real is False


def test_research_finding_model():
    finding = ResearchFinding(
        code="OOS_GAP",
        severity=ResearchFindingSeverity.WARNING,
        component="out_of_sample",
        message="El rendimiento OOS es inferior al rendimiento IS.",
        evidence={"profit_factor_is": 1.8, "profit_factor_oos": 1.2},
    )

    assert finding.code == "OOS_GAP"
    assert finding.severity == ResearchFindingSeverity.WARNING