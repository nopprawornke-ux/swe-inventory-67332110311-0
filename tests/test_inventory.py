import pytest
from inventory import Inventory  # หรือ InventoryService ตามคลาสหลักที่ใช้ใน inventory.py


@pytest.fixture
def empty_inventory():
    """Fixture สร้างคลังสินค้าที่ว่างเปล่า"""
    return Inventory()


# กรณีที่ 1: สินค้าทุกรายการมีจำนวนมากกว่า threshold -> คืน list ว่าง
def test_low_stock_all_above_threshold(empty_inventory):
    inv = empty_inventory
    inv.add_product("Apple", 20)
    inv.add_product("Banana", 15)
    assert inv.low_stock_items(10) == []


# กรณีที่ 2: มีสินค้าที่จำนวนเท่ากับ threshold พอดี -> ต้องถูกนับรวมด้วย (<=)
def test_low_stock_exactly_equal_threshold(empty_inventory):
    inv = empty_inventory
    inv.add_product("Apple", 10)
    inv.add_product("Banana", 20)
    assert inv.low_stock_items(10) == ["Apple"]


# กรณีที่ 3: มีสินค้าเข้าเกณฑ์หลายรายการ -> ผลลัพธ์ต้องเรียงตามชื่อ ไม่ใช่ตามลำดับที่เพิ่ม
def test_low_stock_sorted_by_name(empty_inventory):
    inv = empty_inventory
    inv.add_product("Orange", 3)
    inv.add_product("Apple", 2)
    inv.add_product("Banana", 5)
    # คาดหวังการเรียงตามตัวอักษร: Apple, Banana, Orange
    assert inv.low_stock_items(5) == ["Apple", "Banana", "Orange"]


# กรณีที่ 4: คลังว่าง -> คืน list ว่าง ไม่ใช่ error
def test_low_stock_empty_inventory(empty_inventory):
    inv = empty_inventory
    assert inv.low_stock_items(10) == []


# กรณีที่ 5: threshold เป็น 0 -> คืนเฉพาะสินค้าที่เหลือ 0
def test_low_stock_threshold_zero(empty_inventory):
    inv = empty_inventory
    inv.add_product("Apple", 0)
    inv.add_product("Banana", 5)
    assert inv.low_stock_items(0) == ["Apple"]


# กรณีที่ 6: threshold ติดลบ -> กำหนดให้ raise ValueError หรือคืน list ว่าง (ในที่นี้เลือก raise ValueError)
def test_low_stock_negative_threshold_raises_error(empty_inventory):
    inv = empty_inventory
    inv.add_product("Apple", 5)
    with pytest.raises(ValueError):
        inv.low_stock_items(-1)