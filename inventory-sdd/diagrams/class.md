# Class Diagram: Inventory System

```mermaid
classDiagram
    %% Interface / Protocol
    class Notifier {
        <<interface>>
        +send(message: str) None
    }

    %% Concrete Implementations
    class EmailNotifier {
        +str recipient
        +send(message: str) None
    }

    class SMSNotifier {
        +str phone_number
        +send(message: str) None
    }

    %% Factory Pattern
    class NotifierFactory {
        +create(channel: str, target: str)$ Notifier
    }

    %% Models
    class Category {
        <<enumeration>>
        ELECTRICAL
        PLUMBING
        TOOLS
        OTHER
    }

    class Product {
        +str name
        +str category
        +int quantity
        +float price
        +int threshold
    }

    class StockTransaction {
        +str product_name
        +str action
        +int quantity
        +int remaining_quantity
    }

    %% Business Service
    class InventoryService {
        -dict~str, Product~ _products
        -Notifier _notifier
        +set_notifier(notifier: Notifier) None
        +add_product(product: Product) None
        +get_product(name: str) Product
        +set_threshold(name: str, threshold: int) None
        +receive_stock(name: str, quantity: int) StockTransaction
        +issue_stock(name: str, quantity: int) StockTransaction
        +get_stock_value_report() dict~str, float~
    }

    %% Relationships
    Notifier <|.. EmailNotifier : realization
    Notifier <|.. SMSNotifier : realization
    NotifierFactory ..> Notifier : creates / dependency
    InventoryService o-- Notifier : aggregation / dependency injection
    InventoryService *-- Product : composition (stores)
    InventoryService ..> StockTransaction : dependency (returns)
```
````[cite: 19]

---

### 2. ไฟล์ `diagrams/sequence.md`[cite: 19]
1. คลิกขวาที่โฟลเดอร์ **`diagrams`** แล้วเลือก **New File**[cite: 19]
2. ตั้งชื่อไฟล์ว่า **`sequence.md`** (Path: `inventory-sdd/diagrams/sequence.md`)[cite: 19]
3. คัดลอกเนื้อหาบล็อกโค้ด Mermaid ด้านล่างนี้ไปวาง แล้วกดบันทึก (`Ctrl + S`):

````markdown
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
```
````[cite: 19]



