import pytest

from core.research.base_research_validator import BaseResearchValidator
from core.research.overfitting_detector import OverfittingDetector


def test_base_research_validator_cannot_be_instantiated():
    with pytest.raises(TypeError):
        BaseResearchValidator()


def test_overfitting_detector_implements_base_contract():
    detector = OverfittingDetector()

    assert isinstance(detector, BaseResearchValidator)
    assert hasattr(detector, "analyze")