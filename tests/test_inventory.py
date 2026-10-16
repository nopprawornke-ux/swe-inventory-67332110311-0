import pytest
from inventory import Inventory

@pytest.fixture
def empty_inventory():
    return Inventory()

def test_low_stock_all_above_threshold(empty_inventory):
    inv = empty_inventory
    inv.add_item("Apple", 20, 10.0)
    inv.add_item("Banana", 15, 10.0)
    assert inv.low_stock_items(10) == []

def test_low_stock_exactly_equal_threshold(empty_inventory):
    inv = empty_inventory
    inv.add_item("Apple", 10, 10.0)
    inv.add_item("Banana", 20, 10.0)
    assert inv.low_stock_items(10) == ["Apple"]

def test_low_stock_sorted_by_name(empty_inventory):
    inv = empty_inventory
    inv.add_item("Orange", 3, 10.0)
    inv.add_item("Apple", 2, 10.0)
    inv.add_item("Banana", 5, 10.0)
    assert inv.low_stock_items(5) == ["Apple", "Banana", "Orange"]

def test_low_stock_empty_inventory(empty_inventory):
    inv = empty_inventory
    assert inv.low_stock_items(10) == []

def test_low_stock_threshold_zero(empty_inventory):
    inv = empty_inventory
    inv.add_item("Apple", 0, 10.0)
    inv.add_item("Banana", 5, 10.0)
    assert inv.low_stock_items(0) == ["Apple"]
def test_low_stock_negative_threshold_raises_error(empty_inventory):
    inv = empty_inventory
    inv.add_item("Apple", 5, 10.0)
    with pytest.raises(ValueError):
        inv.low_stock_items(-1)
