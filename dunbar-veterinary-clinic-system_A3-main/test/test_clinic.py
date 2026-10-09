from src.model.client import Client
from src.model.animal import Animal
from src.service.clinic_service import ClinicService
from datetime import datetime

def test_create_appointment():
    # 创建客户
    client1 = Client("Alice", "13800138000", "alice@example.com")
    # 创建宠物
    pet = Animal("Mimi", "Cat", client1)
    # 创建诊所服务实例
    clinic = ClinicService()
    # 创建预约
    appointment_time = datetime(2026, 10, 1, 14, 0)
    app = clinic.create_appointment(client1, pet, appointment_time, "vaccination")

    # 断言测试
    assert app.client.name == "Alice"
    assert app.animal.name == "Mimi"
    assert app.service == "vaccination"
    assert len(clinic.get_all_appointments()) == 1
    print("Test create passed!")

def test_cancel_appointment():
    client1 = Client("Alice", "13800138000", "alice@example.com")
    pet = Animal("Mimi", "Cat", client1)
    clinic = ClinicService()
    appointment_time = datetime(2026, 10, 1, 14, 0)
    app = clinic.create_appointment(client1, pet, appointment_time, "vaccination")
    result = clinic.cancel_appointment(app.appointment_id)
    assert result == True
    assert app.is_cancelled == True
    print("Test cancel passed!")

def test_get_daily_schedule():
    client1 = Client("Alice", "13800138000", "alice@example.com")
    pet = Animal("Mimi", "Cat", client1)
    clinic = ClinicService()
    appointment_time = datetime(2026, 10, 1, 14, 0)
    clinic.create_appointment(client1, pet, appointment_time, "vaccination")
    schedule = clinic.get_daily_schedule(appointment_time.date())
    assert len(schedule) == 1
    print("Test daily schedule passed!")

if __name__ == "__main__":
    test_create_appointment()
    test_cancel_appointment()
    test_get_daily_schedule()
