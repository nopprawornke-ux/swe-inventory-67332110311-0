from typing import Protocol


class Notifier(Protocol):
    """Protocol สำหรับการแจ้งเตือนตามหลัก Dependency Inversion (DIP)"""

    def send(self, message: str) -> None:
        """ส่งข้อความแจ้งเตือน

        Args:
            message: ข้อความที่ต้องการส่ง
        """
        ...


class EmailNotifier:
    """ระบบแจ้งเตือนผ่านช่องทาง Email (จำลองด้วย Print)"""

    def __init__(self, recipient: str) -> None:
        """กำหนดข้อมูลผู้รับผ่าน Constructor (Dependency Injection)"""
        self.recipient = recipient

    def send(self, message: str) -> None:
        """ส่งข้อความแจ้งเตือนทาง Email โดยพิมพ์ข้อความออกทางคอนโซล"""
        print(f"[Email] To: {self.recipient} | {message}")


class SMSNotifier:
    """ระบบแจ้งเตือนผ่านช่องทาง SMS (จำลองด้วย Print)"""

    def __init__(self, phone_number: str) -> None:
        """กำหนดข้อมูลเบอร์โทรศัพท์ผู้รับผ่าน Constructor (Dependency Injection)"""
        self.phone_number = phone_number

    def send(self, message: str) -> None:
        """ส่งข้อความแจ้งเตือนทาง SMS โดยพิมพ์ข้อความออกทางคอนโซล"""
        print(f"[SMS] To: {self.phone_number} | {message}")


class NotifierFactory:
    """Factory สำหรับสร้าง Instance ของ Notifier ตามช่องทางที่กำหนด"""

    @staticmethod
    def create(channel: str, target: str) -> Notifier:
        """สร้าง Notifier ตามประเภทช่องทางและปลายทางที่ระบุ

        Args:
            channel: ช่องทางแจ้งเตือน เช่น 'Email' หรือ 'SMS'
            target: อีเมลหรือเบอร์โทรศัพท์ปลายทาง

        Returns:
            อ็อบเจกต์ที่สอดคล้องกับ Notifier protocol
        """
        channel_upper = channel.upper()
        if channel_upper == "EMAIL":
            return EmailNotifier(recipient=target)
        elif channel_upper == "SMS":
            return SMSNotifier(phone_number=target)
        else:
            raise ValueError(f"ไม่รองรับช่องทางการแจ้งเตือน: {channel}")