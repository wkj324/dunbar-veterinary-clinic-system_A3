from src.service.clinic_service import Clinic
from src.model.client import Client
from src.model.animal import Animal
from src.model.appointment import Appointment

def test_us5_filter_appointment_by_date():
    # US5：按日期筛选预约
    clinic = Clinic()
    client = Client("Alice", "13800138000", "alice@example.com")
    pet = Animal("Mimi", "Cat", owner_id=1)
    clinic.add_client(client)
    clinic.add_animal(pet)

    appt1 = Appointment("2026-10-20", "checkup", client.id, pet.id)
    appt2 = Appointment("2026-10-21", "vaccine", client.id, pet.id)
    clinic.create_appointment(appt1)
    clinic.create_appointment(appt2)

    result = clinic.filter_appointments_by_date("2026-10-20")
    assert len(result) == 1
    assert result[0].date == "2026-10-20"

def test_us6_search_appointment_by_pet_id():
    # US6：根据宠物ID查找预约
    clinic = Clinic()
    client = Client("Alice", "13800138000", "alice@example.com")
    pet = Animal("Mimi", "Cat", owner_id=1)
    clinic.add_client(client)
    clinic.add_animal(pet)

    appt1 = Appointment("2026-10-20", "checkup", client.id, pet.id)
    appt2 = Appointment("2026-10-20", "vaccine", client.id, pet.id)
    clinic.create_appointment(appt1)
    clinic.create_appointment(appt2)

    result = clinic.search_appointment_by_animal(pet.id)
    assert len(result) == 2

def test_us7_get_daily_schedule():
    # US7：获取当日日程
    clinic = Clinic()
    client = Client("Alice", "13800138000", "alice@example.com")
    pet = Animal("Mimi", "Cat", owner_id=1)
    clinic.add_client(client)
    clinic.add_animal(pet)

    appt1 = Appointment("2026-10-20", "checkup", client.id, pet.id)
    clinic.create_appointment(appt1)

    schedule = clinic.get_daily_schedule("2026-10-20")
    assert len(schedule) == 1
