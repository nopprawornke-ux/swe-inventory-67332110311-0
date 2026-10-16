# Sequence Diagram: จ่ายสินค้าจนสต็อกต่ำกว่า Threshold

```mermaid
sequenceDiagram
autonumber
actor Staff as พนักงานคลังสินค้า
participant Service as InventoryService
participant Prod as Product
participant Notifier as Notifier (Email/SMS)

Staff->>Service: issue_stock(name, quantity)
activate Service

Service->>Service: get_product(name)
alt quantity <= 0
    Service-->>Staff: raise ValueError("Invalid quantity")
end

alt quantity > product.quantity
    Service-->>Staff: raise ValueError("Insufficient stock")
end

%% ตัดสต็อก
Service->>Prod: product.quantity -= quantity
Note over Service,Prod: ปรับปรุงยอดคงเหลือใน Memory

%% ตรวจสอบเงื่อนไขแจ้งเตือน
opt product.quantity < product.threshold
    Service->>Notifier: send("Low stock alert: ...")
    activate Notifier
    Note over Notifier: แสดงผลข้อความแจ้งเตือน (Mock)
    Notifier-->>Service: return
    deactivate Notifier
end

Service-->>Staff: return StockTransaction(action="ISSUE", ...)
deactivate Service