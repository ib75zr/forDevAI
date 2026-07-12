import pytest

from utils import calculate_discount


# ── Happy path ──────────────────────────────────────────────────────────

def test_discount_100_20():
    assert calculate_discount(100, 20) == 80.0


def test_discount_50_10():
    assert calculate_discount(50, 10) == 45.0


def test_discount_zero_percentage():
    assert calculate_discount(100, 0) == 100.0


def test_discount_100_percentage():
    assert calculate_discount(100, 100) == 0.0


def test_discount_zero_price():
    assert calculate_discount(0, 50) == 0.0


# ── Validation: negative price ──────────────────────────────────────────

def test_negative_price_raises_value_error():
    with pytest.raises(ValueError, match="price must be non-negative"):
        calculate_discount(-1, 10)


# ── Validation: percentage out of range ─────────────────────────────────

def test_percentage_below_zero_raises_value_error():
    with pytest.raises(ValueError, match="percentage must be between 0 and 100"):
        calculate_discount(100, -1)


def test_percentage_above_100_raises_value_error():
    with pytest.raises(ValueError, match="percentage must be between 0 and 100"):
        calculate_discount(100, 101)
