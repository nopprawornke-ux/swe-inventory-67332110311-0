# AI Iteration Log

## ขั้นที่ 4: ประเมินโค้ดที่สร้างโดยไม่มี Context / ไฟล์กฎ (Baseline)

### ไฟล์ทดสอบ: `src/inventory_no_context.py`

### ปัญหาและจุดอ่อนที่ตรวจพบ (Code Smells & Architectural Issues):
1. **ขาด Type Hints และ Type Annotations:**
   - ฟังก์ชันและพารามิเตอร์ทั้งหมดไม่มีการระบุ Type ทำให้ยากต่อการทำ Static Analysis หรือตรวจสอบความผิดพลาดด้วย mypy/IDE ก่อนรันจริง
2. **ละเมิด Single Responsibility Principle (SRP):**
   - คลาส `InventorySystem` รับผิดชอบมากเกินไป ทั้งการจัดการสต็อกสินค้า, การคำนวณและสรุปรายงานมูลค่า, รวมถึงการเลือกช่องทางและสั่งส่งข้อความแจ้งเตือน
3. **Hardcode ข้อมูลการส่งข้อความไว้ในระบบ:**
   - มีการระบุอีเมล `manager@company.com` และเบอร์โทรศัพท์ `081-234-5678` ฝังไว้ในตัวแปรของคลาสโดยตรง ทำให้ไม่สามารถยืดหยุ่นต่อการเปลี่ยนผู้รับหรือดึงจากไฟล์คอนฟิกภายนอก
4. **ละเมิด Open/Closed Principle (OCP):**
   - เมธอด `send_alert()` ใช้วิธีตรวจจับช่องทางแบบ `if-elif` หากต้องการเพิ่มช่องทางการแจ้งเตือนใหม่ (เช่น LINE Notify หรือ Webhook) จะต้องแก้ไขโค้ดเดิมในคลาสหลักเสมอ
5. **โครงสร้างข้อมูลขาดความเป็น Object-Oriented:**
   - การเก็บข้อมูลสินค้าใช้ Dictionary แบบดิบ ทำให้ไม่มี Schema แน่นอน และเสี่ยงต่อการอ้างอิง Key ผิดพลาด
```[cite: 13]

---

#### สเต็ปที่ 3: เช็กโครงสร้างไฟล์ใน VS Code
แถบ Explorer ด้านซ้ายของคุณจะต้องมีหน้าตาเป็นแบบนี้:
```text
inventory-sdd/
├── diagrams/
├── specs/
│   └── spec.md
├── src/
│   └── inventory_no_context.py
└── AI_ITERATION_LOG.md
```[cite: 11, 13]

---

#### สเต็ปที่ 4: สั่งบันทึกและส่งขึ้น GitHub ด้วย Git
เปิด Terminal ใน VS Code แล้วพิมพ์คำสั่งเหล่านี้ทีละบรรทัด:

```powershell
git add src/inventory_no_context.py AI_ITERATION_LOG.md
git commit -m "feat: เพิ่ม inventory_no_context.py และบันทึกปัญหาลงใน AI_ITERATION_LOG.md"
git push
```[cite: 13]

หลังจากรันเสร็จ ก็จะพร้อมเข้าสู่ขั้นตอนที่ 5 (การสร้างไฟล์กฎ context / rule เพื่อให้ AI เขียนโค้ดที่มีคุณภาพ) ได้ทันทีครับ