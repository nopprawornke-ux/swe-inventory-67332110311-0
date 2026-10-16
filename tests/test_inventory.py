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
# ==========================================
# ขั้นที่ 4: Tests เสริมสำหรับเมธอด sell
# ==========================================


# 1. ค่าขอบ: ขายเท่ากับจำนวนที่มีอยู่ทั้งหมด ผลลัพธ์ต้องเหลือ 0 พอดี
def test_sell_exact_boundary_to_zero(empty_inventory):
    inv = empty_inventory
    inv.add_item("Apple", 10, 15.0)
    remaining = inv.sell("Apple", 10)
    assert remaining == 0
    assert inv._items["Apple"].quantity == 0


# 2. ค่าที่ไม่ควรรับ: ขายจำนวน 0 หรือติดลบ ต้องเกิด ValueError
def test_sell_zero_or_negative_amount_raises_error(empty_inventory):
    inv = empty_inventory
    inv.add_item("Apple", 10, 15.0)
    with pytest.raises(ValueError, match="จำนวนที่ขายต้องมากกว่าศูนย์"):
        inv.sell("Apple", 0)
    with pytest.raises(ValueError, match="จำนวนที่ขายต้องมากกว่าศูนย์"):
        inv.sell("Apple", -5)


# 3. ค่าที่ไม่ควรรับ: ขายเกินจำนวนที่มีอยู่ ต้องเกิด ValueError พร้อมข้อความเตือน
def test_sell_exceeds_available_quantity(empty_inventory):
    inv = empty_inventory
    inv.add_item("Apple", 5, 15.0)
    with pytest.raises(ValueError, match="ไม่เพียงพอสำหรับการขาย"):
        inv.sell("Apple", 6)


# 4. เส้นทาง error: ขายสินค้าที่ไม่มีในคลัง ต้องเกิด KeyError
def test_sell_nonexistent_product_raises_key_error(empty_inventory):
    inv = empty_inventory
    with pytest.raises(KeyError, match="ไม่พบสินค้า"):
        inv.sell("NonExistentItem", 1)


# 5. ชนิดข้อมูล: ใส่จำนวนที่ขายเป็นสตริงหรือทศนิยม ต้องป้องกันชนิดข้อมูลผิดพลาด
def test_sell_invalid_type_raises_type_error(empty_inventory):
    inv = empty_inventory
    inv.add_item("Apple", 10, 15.0)
    with pytest.raises(TypeError):
        inv.sell("Apple", "two")

        import pytest
from inventory import Inventory, InventoryItem


# ทดสอบเงื่อนไข Validation ของ InventoryItem
def test_inventory_item_validations():
    with pytest.raises(ValueError, match="ชื่อสินค้าต้องไม่ว่างเปล่า"):
        InventoryItem("", 5, 10.0)
    with pytest.raises(ValueError, match="จำนวนสินค้าต้องไม่ติดลบ"):
        InventoryItem("Item", -1, 10.0)
    with pytest.raises(ValueError, match="ราคาต้องมากกว่าศูนย์"):
        InventoryItem("Item", 5, 0.0)


# ทดสอบกรณีเพิ่มสินค้าชื่อซ้ำใน Inventory
def test_add_duplicate_item_raises_error(empty_inventory):
    inv = empty_inventory
    inv.add_item("Apple", 5, 10.0)
    with pytest.raises(ValueError, match="มีอยู่ในระบบแล้ว"):
        inv.add_item("Apple", 2, 10.0)


# ทดสอบเมธอด restock ทั้งกรณีปกติและกรณี error
def test_restock_cases(empty_inventory):
    inv = empty_inventory
    inv.add_item("Apple", 5, 10.0)

    # เติมปกติ
    new_qty = inv.restock("Apple", 10)
    assert new_qty == 15
    assert inv._items["Apple"].quantity == 15

    # สินค้าไม่มีในระบบ
    with pytest.raises(KeyError, match="ไม่พบสินค้า"):
        inv.restock("Orange", 5)

    # เติมค่าติดลบหรือศูนย์
    with pytest.raises(ValueError, match="ต้องมากกว่าศูนย์"):
        inv.restock("Apple", 0)
    with pytest.raises(ValueError, match="ต้องมากกว่าศูนย์"):
        inv.restock("Apple", -3)


# ทดสอบเมธอด get_total_value
def test_get_total_value(empty_inventory):
    inv = empty_inventory
    assert inv.get_total_value() == 0.0

    inv.add_item("Apple", 10, 15.0)  # 150.0
    inv.add_item("Banana", 5, 20.0)  # 100.0
    assert inv.get_total_value() == 250.0