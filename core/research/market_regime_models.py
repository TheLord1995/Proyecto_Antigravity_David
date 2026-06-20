"""
Modelos para detección automática de régimen de mercado.

No ejecuta operaciones.
No aprueba operativa real.
"""

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class MarketRegime(str, Enum):
    TRENDING = "TRENDING"
    RANGING = "RANGING"
    HIGH_VOLATILITY = "HIGH_VOLATILITY"
    LOW_VOLATILITY = "LOW_VOLATILITY"
    MIXED = "MIXED"
    INSUFFICIENT_DATA = "INSUFFICIENT_DATA"


class OHLCVRecord(BaseModel):
    timestamp: str
    open: float = Field(..., gt=0)
    high: float = Field(..., gt=0)
    low: float = Field(..., gt=0)
    close: float = Field(..., gt=0)
    volume: Optional[float] = None


class MarketRegimeResult(BaseModel):
    regime: MarketRegime
    confidence: float = Field(..., ge=0.0, le=1.0)
    adx: Optional[float] = None
    atr: Optional[float] = None
    atr_pct: Optional[float] = None
    volatility_pct: Optional[float] = None
    candles_analyzed: int
    reason: str
    approved_for_real: bool = False