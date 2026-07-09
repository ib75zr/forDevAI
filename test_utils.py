from utils import calculate_discount


def test_discount_100_20():
    assert calculate_discount(100, 20) == 80.0


def test_discount_50_10():
    assert calculate_discount(50, 10) == 45.0
