class InventorySystem:
    def __init__(self):
        # จัดเก็บข้อมูลสินค้าไว้ใน memory dictionary
        self.items = {}
        # hardcode ช่องทางการแจ้งเตือนและข้อมูลผู้รับ
        self.notification_channel = "Email"
        self.manager_email = "manager@company.com"
        self.manager_phone = "081-234-5678"

    def add_product(self, name, category, quantity, price, threshold):
        self.items[name] = {
            "category": category,
            "quantity": quantity,
            "price": price,
            "threshold": threshold,
        }

    def receive_stock(self, name, quantity):
        if quantity <= 0:
            raise ValueError("Invalid quantity")
        if name not in self.items:
            raise KeyError("Product not found")
        self.items[name]["quantity"] += quantity
        return self.items[name]["quantity"]

    def issue_stock(self, name, quantity):
        if quantity <= 0:
            raise ValueError("Invalid quantity")
        if name not in self.items:
            raise KeyError("Product not found")

        current_stock = self.items[name]["quantity"]
        if quantity > current_stock:
            raise ValueError("Insufficient stock")

        # ตัดยอดสต็อก
        self.items[name]["quantity"] -= quantity
        remaining = self.items[name]["quantity"]

        # ตรวจสอบและแจ้งเตือนเมื่อต่ำกว่าหรือเท่ากับ threshold
        if remaining <= self.items[name]["threshold"]:
            self.send_alert(name, remaining)

        return remaining

    def set_threshold(self, name, threshold):
        if name not in self.items:
            raise KeyError("Product not found")
        self.items[name]["threshold"] = threshold

    def set_notification_channel(self, channel):
        self.notification_channel = channel

    def send_alert(self, name, remaining):
        message = f"Low stock alert: {name} (remaining: {remaining})"
        if self.notification_channel == "Email":
            print(f"Sending Email to {self.manager_email}: {message}")
        elif self.notification_channel == "SMS":
            print(f"Sending SMS to {self.manager_phone}: {message}")
        else:
            print(message)

    def get_stock_value_report(self):
        report = {}
        total_value = 0
        for item in self.items.values():
            cat = item["category"]
            val = item["quantity"] * item["price"]
            report[cat] = report.get(cat, 0) + val
            total_value += val
        report["total"] = total_value
        return report
