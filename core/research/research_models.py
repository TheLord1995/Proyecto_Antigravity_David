"""
core/research/research_models.py
--------------------------------
Contratos Pydantic para la capa de investigación cuantitativa de Antigravity 2.0.

Esta capa NO ejecuta operaciones, NO aprueba operativa real y NO sustituye al RiskEngine.
Su responsabilidad es evaluar robustez investigadora antes de permitir paper trading
o revisión humana posterior.
"""
from datetime import UTC, datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, model_validator


class ResearchStatus(str, Enum):
    REJECTED = "REJECTED"
    FRAGILE = "FRAGILE"
    NEEDS_REVIEW = "NEEDS_REVIEW"
    PROMISING = "PROMISING"
    RESEARCH_APPROVED = "RESEARCH_APPROVED"
    PAPER_TRADING_READY = "PAPER_TRADING_READY"


class ResearchFindingSeverity(str, Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"


class ResearchFinding(BaseModel):
    code: str = Field(..., min_length=2)
    severity: ResearchFindingSeverity
    message: str = Field(..., min_length=5)
    component: str = Field(
        ...,
        description="Componente que genera el hallazgo: overfitting, walk_forward, regime, stress, etc.",
    )
    evidence: Dict[str, Any] = Field(default_factory=dict)


class ResearchValidationInput(BaseModel):
    strategy_id: str = Field(..., min_length=3)
    report_hash_sha256: str = Field(..., min_length=64, max_length=64)

    symbol: Optional[str] = None
    timeframe: Optional[str] = None

    total_trades: int = Field(..., ge=0)
    profit_factor_is: Optional[float] = None
    profit_factor_oos: Optional[float] = None
    max_drawdown_pct: Optional[float] = Field(default=None, ge=0)
    sharpe_ratio: Optional[float] = None
    expectancy: Optional[float] = None

    has_in_sample: bool = False
    has_out_of_sample: bool = False
    has_walk_forward: bool = False
    walk_forward_windows: int = Field(default=0, ge=0)
    walk_forward_passed_windows: int = Field(default=0, ge=0)
    walk_forward_success_rate: Optional[float] = Field(default=None, ge=0, le=100)
    has_real_ticks: bool = False
    includes_spread: bool = False
    includes_commissions: bool = False
    includes_slippage: bool = False

    tested_assets: List[str] = Field(default_factory=list)
    tested_regimes: List[str] = Field(default_factory=list)

    metadata: Dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="after")
    def validate_no_real_execution_flags(self):
        forbidden_keys = {
            "approved_for_real",
            "allow_real_execution",
            "real_execution",
            "send_order",
        }

        metadata_keys = {str(k).lower() for k in self.metadata.keys()}
        forbidden_found = forbidden_keys.intersection(metadata_keys)

        if forbidden_found:
            raise ValueError(
                f"ResearchValidationInput no puede contener flags de ejecución real: {forbidden_found}"
            )

        return self


class ResearchValidationResult(BaseModel):
    strategy_id: str
    status: ResearchStatus
    findings: List[ResearchFinding] = Field(default_factory=list)

    research_score: float = Field(..., ge=0, le=100)
    eligible_for_paper_trading: bool = False

    approved_for_real: bool = Field(
        default=False,
        description="Inmutable: la capa research nunca aprueba ejecución real.",
    )

    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    metadata: Dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="after")
    def enforce_safety_invariants(self):
        if self.approved_for_real is not False:
            raise ValueError(
                "ResearchValidationResult nunca puede aprobar ejecución real."
            )

        if self.status == ResearchStatus.PAPER_TRADING_READY:
            self.eligible_for_paper_trading = True

        return self