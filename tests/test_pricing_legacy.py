import datetime

import pytest

import pricing
from pricing import calc


@pytest.fixture(autouse=True)
def reset_globals():
    pricing.member_points.clear()
    pricing.LOG.clear()
    yield
    pricing.member_points.clear()
    pricing.LOG.clear()


def test_normal_price_single_item():
    items = [("Pen", 1, 100.0)]
    assert calc(items) == 107.0


def test_bulk_discount_threshold_50():
    items = [("Book", 50, 10.0)]
    assert calc(items) == 508.25


def test_bulk_discount_threshold_100():
    items = [("Pencil", 100, 10.0)]
    assert calc(items) == 963.0


def test_item_quantity_zero():
    items = [("Eraser", 0, 50.0)]
    assert calc(items) == 0.0


def test_member_discount_and_points():
    items = [("Bag", 1, 1000.0)]
    result = calc(items, member="Somchai")
    assert result == 1016.5
    assert pricing.member_points["Somchai"] == 9


def test_coupon_save50():
    items = [("Pen", 2, 100.0)]
    assert calc(items, coupon="SAVE50") == 160.5


def test_coupon_half():
    items = [("Pen", 2, 100.0)]
    assert calc(items, coupon="HALF") == 107.0


def test_coupon_newyear_in_january():
    items = [("Pen", 2, 100.0)]
    jan_date = datetime.date(2026, 1, 15)
    assert calc(items, coupon="NEWYEAR", today=jan_date) == 171.2


def test_coupon_newyear_outside_january():
    items = [("Pen", 2, 100.0)]
    feb_date = datetime.date(2026, 2, 15)
    assert calc(items, coupon="NEWYEAR", today=feb_date) == 214.0


def test_discount_greater_than_total_price():
    items = [("Ruler", 1, 30.0)]
    assert calc(items, coupon="SAVE50") == 0.0


def test_log_recording_side_effect():
    items = [("Pen", 1, 100.0)]
    result = calc(items, member="Alice")
    assert len(pricing.LOG) == 1
    assert pricing.LOG[0] == ("Alice", result)
