"""
pricing.py - โมดูลคำนวณราคาและส่วนลด (Refactored Version)
"""

import datetime
from typing import Any

TAX_RATE = 0.07
MEMBER_DISCOUNT_RATE = 0.05
NEWYEAR_DISCOUNT_RATE = 0.20
HALF_DISCOUNT_RATE = 0.50
SAVE50_DISCOUNT_AMOUNT = 50.0

member_points: dict[str, int] = {}
LOG: list[tuple[Any, float]] = []


def _calculate_item_subtotal(quantity: int, unit_price: float) -> float:
    if quantity <= 0:
        return 0.0
    subtotal = quantity * unit_price
    if quantity >= 100:
        return subtotal * 0.90
    elif quantity >= 50:
        return subtotal * 0.95
    return subtotal


def _apply_member_benefit(total: float, member: str | None) -> float:
    if member is None:
        return total
    if member not in member_points:
        member_points[member] = 0
    discounted_total = total * (1.0 - MEMBER_DISCOUNT_RATE)
    earned_points = int(discounted_total / 100)
    member_points[member] += earned_points
    return discounted_total


def _apply_coupon(total: float, coupon: str | None, today: datetime.date | None) -> float:
    if coupon is None:
        return total
    if coupon == "SAVE50":
        return total - SAVE50_DISCOUNT_AMOUNT
    elif coupon == "HALF":
        return total * HALF_DISCOUNT_RATE
    elif coupon == "NEWYEAR":
        current_date = datetime.date.today() if today is None else today
        if current_date.month == 1:
            return total * (1.0 - NEWYEAR_DISCOUNT_RATE)
    return total


def calc(
    items: list[tuple[str, int, float]],
    member: str | None = None,
    coupon: str | None = None,
    today: datetime.date | None = None,
) -> float:
    subtotal = sum(_calculate_item_subtotal(quantity=item[1], unit_price=item[2]) for item in items)
    subtotal = _apply_member_benefit(subtotal, member)
    subtotal = _apply_coupon(subtotal, coupon, today)
    if subtotal < 0:
        subtotal = 0.0
    total_with_tax = subtotal + (subtotal * TAX_RATE)
    final_amount = round(total_with_tax, 2)
    LOG.append((member, final_amount))
    return final_amount
