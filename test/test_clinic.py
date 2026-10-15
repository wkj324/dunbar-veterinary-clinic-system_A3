from datetime import datetime, date
from src.service.clinic_service import ClinicService
from src.model.client import Client
from src.model.animal import Animal


def test_create_appointment():
    # 创建客户实例
    client1 = Client("Alice", "13800138000", "alice@example.com")
    # Animal参数：animal_id, name, species, owner_id
    pet = Animal(1, "Mimi", "Cat", 1)
    clinic = ClinicService()
    # start_time 必须是datetime对象
    appt_time = datetime(2026, 10, 10, 9, 0)
    appt = clinic.create_appointment(client1, pet, appt_time, "in-clinic")
    all_appts = clinic.get_all_appointments()
    assert len(all_appts) == 1
    assert appt.client == client1
    assert appt.animal == pet


def test_cancel_appointment():
    client1 = Client("Alice", "13800138000", "alice@example.com")
    pet = Animal(1, "Mimi", "Cat", 1)
    clinic = ClinicService()
    appt_time = datetime(2026, 10, 10, 9, 0)
    appt = clinic.create_appointment(client1, pet, appt_time, "in-clinic")
    # 执行取消
    result = clinic.cancel_appointment(appt.appointment_id)
    assert result is True
    all_appts = clinic.get_all_appointments()
    assert len(all_appts) == 1
    assert appt.is_cancelled is True


def test_get_daily_schedule():
    client1 = Client("Alice", "13800138000", "alice@example.com")
    pet = Animal(1, "Mimi", "Cat", 1)
    clinic = ClinicService()
    appt_time = datetime(2026, 10, 10, 9, 0)
    clinic.create_appointment(client1, pet, appt_time, "in-clinic")
    # 查询当天预约
    target_day = date(2026, 10, 10)
    daily_appts = clinic.get_daily_schedule(target_day)
    assert len(daily_appts) == 1