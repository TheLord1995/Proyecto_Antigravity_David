"""
Tests del MarketRegimeDetector.

Valida detección automática de régimen desde velas OHLCV.
"""

from copy import deepcopy

from core.research.market_regime_detector import MarketRegimeDetector
from core.research.market_regime_models import MarketRegime, OHLCVRecord


def build_trending_candles(count: int = 40) -> list[OHLCVRecord]:
    candles = []
    price = 100.0

    for index in range(count):
        open_price = price
        close_price = price + 1.0
        high_price = close_price + 0.4
        low_price = open_price - 0.2

        candles.append(
            OHLCVRecord(
                timestamp=f"2026-01-{(index % 28) + 1:02d}",
                open=open_price,
                high=high_price,
                low=low_price,
                close=close_price,
                volume=1000,
            )
        )

        price = close_price

    return candles


def build_ranging_candles(count: int = 40) -> list[OHLCVRecord]:
    candles = []
    base_price = 100.0

    for index in range(count):
        offset = 0.15 if index % 2 == 0 else -0.15
        open_price = base_price
        close_price = base_price + offset
        high_price = max(open_price, close_price) + 0.10
        low_price = min(open_price, close_price) - 0.10

        candles.append(
            OHLCVRecord(
                timestamp=f"2026-02-{(index % 28) + 1:02d}",
                open=open_price,
                high=high_price,
                low=low_price,
                close=close_price,
                volume=1000,
            )
        )

    return candles


def build_high_volatility_candles(count: int = 40) -> list[OHLCVRecord]:
    candles = []
    price = 100.0

    for index in range(count):
        open_price = price
        close_price = price + (2.0 if index % 2 == 0 else -2.0)
        high_price = max(open_price, close_price) + 4.0
        low_price = min(open_price, close_price) - 4.0

        candles.append(
            OHLCVRecord(
                timestamp=f"2026-03-{(index % 28) + 1:02d}",
                open=open_price,
                high=high_price,
                low=low_price,
                close=close_price,
                volume=1000,
            )
        )

        price = close_price

    return candles


def test_detects_insufficient_data():
    detector = MarketRegimeDetector()
    candles = build_trending_candles(count=10)

    result = detector.detect(candles)

    assert result.regime == MarketRegime.INSUFFICIENT_DATA
    assert result.confidence == 1.0
    assert result.approved_for_real is False


def test_detects_trending_market():
    detector = MarketRegimeDetector()
    candles = build_trending_candles()

    result = detector.detect(candles)

    assert result.regime == MarketRegime.TRENDING
    assert result.adx is not None
    assert result.adx >= detector.ADX_TRENDING_THRESHOLD
    assert result.approved_for_real is False


def test_detects_ranging_market():
    detector = MarketRegimeDetector()
    candles = build_ranging_candles()

    result = detector.detect(candles)

    assert result.regime == MarketRegime.RANGING
    assert result.adx is not None
    assert result.adx < detector.ADX_RANGING_THRESHOLD
    assert result.approved_for_real is False


def test_detects_high_volatility_market():
    detector = MarketRegimeDetector()
    candles = build_high_volatility_candles()

    result = detector.detect(candles)

    assert result.regime == MarketRegime.HIGH_VOLATILITY
    assert result.atr_pct is not None
    assert result.atr_pct >= detector.HIGH_ATR_PCT_THRESHOLD
    assert result.approved_for_real is False


def test_result_never_approves_real_execution():
    detector = MarketRegimeDetector()
    candles = build_trending_candles()

    result = detector.detect(candles)

    assert result.approved_for_real is False


def test_detector_does_not_mutate_input():
    detector = MarketRegimeDetector()
    candles = build_trending_candles()
    original = deepcopy(candles)

    detector.detect(candles)

    assert candles == original