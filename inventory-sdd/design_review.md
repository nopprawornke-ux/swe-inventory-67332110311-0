# การตรวจประเมินการออกแบบตามหลัก SOLID Principles

| หลัก SOLID | ละเมิดหรือไม่ | class หรือ method ที่เกี่ยวข้อง | อธิบายและผลกระทบ | ข้อเสนอปรับปรุง |
|---|---|---|---|---|
| **S (SRP)**<br>Single Responsibility Principle | **ไม่ละเมิด** | `InventoryService`<br>`EmailNotifier`<br>`SMSNotifier` | แต่ละ Class มีหน้าที่เดียวชัดเจน โดย `InventoryService` จัดการเฉพาะ Business Logic คลังสินค้า, Notifier ทำหน้าที่ส่งข้อความ, และ Models เก็บข้อมูล ไม่มี method ไหนที่คำนวณปนกับ I/O โดยตรง | ปัจจุบันแยกชั้นความรับผิดชอบได้ดีแล้ว หากในอนาคตมี Logic การทำ Report ซับซ้อนขึ้น สามารถแยก `ReportService` ออกมาเพิ่มได้ |
| **O (OCP)**<br>Open/Closed Principle | **ไม่ละเมิด** | `InventoryService`<br>`NotifierFactory` | `InventoryService` ไม่ผูกมัดกับช่องทางแจ้งเตือน และไม่มีเงื่อนไข `if-elif` ตรวจสอบประเภทช่องทาง ทำให้เมื่อต้องการเพิ่มช่องทางใหม่ (เช่น LINE, Slack) สามารถสร้าง Notifier ใหม่มาต่อเชื่อมได้ทันทีโดยไม่ต้องแก้โค้ดใน Service | นำ Registry Pattern มาใช้ร่วมกับ `NotifierFactory` แทน `if-elif` เพื่อให้การขยายช่องทางใหม่ไม่ต้องแก้ Factory ด้วย |
| **L (LSP)**<br>Liskov Substitution Principle | **ไม่ละเมิด** | `EmailNotifier`<br>`SMSNotifier`<br>(ผ่าน `Notifier` Protocol) | ทั้ง `EmailNotifier` และ `SMSNotifier` ปฏิบัติตาม Interface ของ `Notifier` Protocol โดยมี method `send(message: str) -> None` เหมือนกัน สามารถนำไปทดแทนกันได้ 100% โดยที่ `InventoryService` ยังคงทำงานได้ถูกต้องสมบูรณ์ | รักษา Signature และ Exception behavior ของ method `send()` ให้เป็นมาตรฐานเดียวกันในทุก Notifier |
| **I (ISP)**<br>Interface Segregation Principle | **ไม่ละเมิด** | `Notifier` Protocol | `Notifier` Protocol มีเพียง method เดียวคือ `send(message: str)` ซึ่งเป็นสิ่งที่ Client จำเป็นต้องใช้จริงๆ ไม่มี method ส่วนเกินที่บีบให้ Class ลูกต้อง implement สิ่งที่ไม่จำเป็น | คงความเป็น Lean Interface เช่นนี้ไว้ หากมีฟีเจอร์เพิ่มเติม เช่น การดึงประวัติการส่ง ให้แยกเป็น Protocol อื่นต่างหาก |
| **D (DIP)**<br>Dependency Inversion Principle | **ไม่ละเมิด** | `InventoryService.__init__()`<br>`InventoryService.set_notifier()` | High-level module (`InventoryService`) ไม่ได้ import หรือรู้จัก Low-level modules (`EmailNotifier`, `SMSNotifier`) โดยตรง แต่ขึ้นต่อ Abstraction คือ `Notifier` Protocol ผ่าน Constructor Injection | ปัจจุบันทำ Dependency Injection ผ่าน Constructor ถูกต้องสมบูรณ์ตามหลัก DIP แล้ว |
```[cite: 17]

---

### จุดสำคัญสำหรับเตรียมตอบเมื่ออาจารย์สุ่มถามในคาบ[cite: 17]

1. **ทำไมระบบถึงไม่ละเมิด OCP?**[cite: 17]
   * **คำตอบ:** เพราะใน `InventoryService` ไม่มีคำสั่ง `if channel == "email": ... elif channel == "sms": ...`[cite: 17] ตัว Service สั่งแค่ `self._notifier.send(...)` ทำให้เราสามารถเขียนคลาสแจ้งเตือนแบบใหม่ขึ้นมา แล้วส่งเข้ามาใช้งานได้ทันทีโดยไม่ต้องแก้ Service เดิมแม้แต่บรรทัดเดียว[cite: 17]
2. **ทำไมถึงไม่ละเมิด DIP?**[cite: 17]
   * **คำตอบ:** ในไฟล์ `service.py` บรรทัดบนสุด เรา `from notifiers import Notifier` ซึ่งเป็น Interface (Protocol)[cite: 17] ไม่ได้มีการ `import EmailNotifier` หรือ `SMSNotifier` เข้ามาเลย[cite: 17] และเรารับ Notifier เข้ามาผ่าน Constructor (`Dependency Injection`)[cite: 14]
3. **ทำไมถึงไม่ละเมิด SRP?**[cite: 17]
   * **คำตอบ:** เราแยกไฟล์ชัดเจน `models.py` จัดการข้อมูล, `service.py` จัดการ Logic, และ `notifiers.py` จัดการเรื่องส่งข้อความ ไม่มี Method ไหนที่ทั้งคำนวณและสั่ง Print ส่งข้อความเองในจุดเดียว[cite: 14, 17]

---

### คำสั่ง Git สำหรับส่งงานในขั้นตอนนี้
บันทึกไฟล์ `design_review.md` แล้วรันใน Terminal[cite: 17]:

```powershell
git add design_review.md
git commit -m "docs: เพิ่มรายงานการตรวจประเมิน SOLID ลงใน design_review.md"
git push
```[cite: 17]

<Elicitations message="มีขั้นตอนไหนในแลปที่ต้องการทำต่อไหมครับ?">
  <Elicitation label="ส่งภาพขั้นตอนถัดไป" query="นี่คือขั้นตอนถัดไปของ Lab ช่วยแนะนำวิธีทำต่อ"/>
  <Elicitation label="ตรวจไฟล์ทั้งหมดใน Git" query="ขอคำสั่งเช็กความเรียบร้อยของ Git ก่อนส่งแลปทั้งหมด"/>
</Elicitations>