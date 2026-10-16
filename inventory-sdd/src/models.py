from dataclasses import dataclass
from enum import StrEnum


class Category(StrEnum):
    """หมวดหมู่สินค้าในระบบ"""

    ELECTRICAL = "ไฟฟ้า"
    PLUMBING = "ประปา"
    TOOLS = "เครื่องมือช่าง"
    OTHER = "ทั่วไป"


@dataclass
class Product:
    """ข้อมูลสินค้าในคลัง

    Attributes:
        name: ชื่อสินค้า
        category: หมวดหมู่สินค้า
        quantity: จำนวนสินค้าคงเหลือ
        price: ราคาต่อหน่วย (บาท)
        threshold: เกณฑ์จำนวนสต็อกขั้นต่ำสำหรับการแจ้งเตือน
    """

    name: str
    category: str
    quantity: int
    price: float
    threshold: int


@dataclass
class StockTransaction:
    """ข้อมูลประวัติการรับเข้าและจ่ายออกสินค้า

    Attributes:
        product_name: ชื่อสินค้า
        action: ประเภทรายการ ('RECEIVE' หรือ 'ISSUE')
        quantity: จำนวนที่มีการรับหรือจ่าย
        remaining_quantity: จำนวนคงเหลือหลังทำรายการ
    """

    product_name: str
    action: str
    quantity: int
    remaining_quantity: int
