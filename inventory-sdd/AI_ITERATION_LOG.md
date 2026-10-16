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

## ขั้นที่ 6: ตารางเปรียบเทียบผลลัพธ์ก่อนและหลังมี Context (.ai-rules.md)

| ประเด็น | ขั้นที่ 4 ก่อนมี context | ขั้นที่ 6 หลังมี context |
|---|---|---|
| **แยกไฟล์และแยกหน้าที่หรือไม่** | ไม่แยก รวมทุกอย่างไว้ในคลาสเดียวใน `src/inventory_no_context.py` (ละเมิด SRP) | แยกชัดเจน 3 ไฟล์: `models.py` (Data), `notifiers.py` (Notification), `service.py` (Business Logic) ตามหลัก SRP |
| **มี type hint และ docstring หรือไม่** | ไม่มี type annotation กำกับ และไม่มี docstring อธิบายฟังก์ชัน | มี type hints ครบทุก function signature และมี docstrings ภาษาไทยอธิบาย public methods ทั้งหมด |
| **service ผูกกับ notifier ตรง ๆ หรือไม่** | ผูกตรงในคลาส มีคำสั่ง if/elif แยกประเภทแจ้งเตือนในตัว | ไม่ผูกตรง ใช้ Notifier Protocol (DIP) และรับ dependency ผ่าน Constructor |
| **hardcode config หรือไม่** | มีการ hardcode อีเมลและเบอร์โทรศัพท์ไว้ในคลาสโดยตรง | ไม่ hardcode รับค่าปลายทางผ่าน Notifier constructor และ Factory Pattern |
```[cite: 17]

## ขั้นที่ 7: บันทึกการวนลูปแก้ที่ Spec หรือ Context (Iteration Log)

### รอบที่ 1: การแจ้งเตือนเมื่อสต็อกเท่ากับ threshold พอดี
1. **ผลที่ผิด:** โค้ดเดิมแจ้งเตือนเมื่อสต็อกเหลือเท่ากับ threshold พอดี (`<=`) ทั้งที่ความต้องการจริงคือแจ้งเตือนเฉพาะเมื่อต่ำกว่าเท่านั้น (`<`)
2. **สาเหตุ:** อยู่ที่ **`specs/spec.md`** เนื่องจาก Scenario เขียนกำกวม ไม่ได้ระบุเคสเท่ากับ threshold ไว้อย่างชัดเจน
3. **แก้ที่ spec หรือ context อย่างไร:** เพิ่ม Scenario ใน `specs/spec.md` (US-02) ระบุชัดเจนว่ากรณีจ่ายจนสต็อกเหลือเท่ากับ threshold พอดี ระบบต้องไม่ส่งการแจ้งเตือน
4. **ผลหลังแก้:** ปรับแก้ Logic ใน `src/service.py` เป็น `quantity < threshold` เมื่อรันเคสสต็อกเท่ากับเกณฑ์ ระบบจะไม่ส่งการแจ้งเตือน ถูกต้องตามเกณฑ์

### รอบที่ 2: ความแม่นยำของทศนิยมในรายงานมูลค่าสต็อก (Financial Precision)
1. **ผลที่ผิด:** ตัวเลขสรุปมูลค่าสินค้าในรายงานเป็น float ดิบ อาจเกิดปัญหาเศษทศนิยมลอย (floating-point precision issue)
2. **สาเหตุ:** อยู่ที่ **`.ai-rules.md`** ไม่ได้ระบุข้อกำหนดในการจัดการทศนิยมของตัวเลขการเงิน
3. **แก้ที่ spec หรือ context อย่างไร:** เพิ่มกฎใน `.ai-rules.md` บังคับให้รายงานตัวเลขมูลค่าสินค้าทุกประเภทต้องปัดทศนิยม 2 ตำแหน่งด้วย `round(val, 2)`
4. **ผลหลังแก้:** เมธอด `get_stock_value_report()` ใน `src/service.py` คืนค่าที่ปัดทศนิยม 2 ตำแหน่งเรียบร้อย สอดคล้องกับมาตรฐาน
```[cite: 14, 18]

---

### 5. สั่ง Commit และ Push งานขึ้น Git[cite: 18]
เปิด Terminal ใน VS Code แล้วพิมพ์คำสั่งตามที่โจทย์กำหนด[cite: 18]:

```powershell
git add src/ specs/spec.md .ai-rules.md AI_ITERATION_LOG.md
git commit -m "feat: implement ฟีเจอร์แจ้งเตือน+รายงานจาก spec พร้อมบันทึก iteration"
git push
```[cite: 18]