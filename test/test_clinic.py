from src.service.clinic_service import Clinic
from src.model.client import Client
from src.model.animal import Animal
from src.model.appointment import Appointment

def test_create_appointment():
    client1 = Client("Alice", "13800138000", "alice@example.com")
    pet = Animal("Mimi", "Cat", owner_id=client1.id)
    clinic = Clinic()
    clinic.add_client(client1)
    clinic.add_animal(pet)
    appt = Appointment("2026-10-10", "in-clinic", client1.id, pet.id)
    clinic.create_appointment(appt)
    all_appts = clinic.get_all_appointments()
    assert len(all_appts) == 1
    assert all_appts[0].pet_id == pet.id

def test_cancel_appointment():
    client1 = Client("Alice", "13800138000", "alice@example.com")
    pet = Animal("Mimi", "Cat", owner_id=client1.id)
    clinic = Clinic()
    clinic.add_client(client1)
    clinic.add_animal(pet)
    appt = Appointment("2026-10-10", "in-clinic", client1.id, pet.id)
    clinic.create_appointment(appt)
    clinic.cancel_appointment(appt.id)
    all_appts = clinic.get_all_appointments()
    assert len(all_appts) == 0

def test_get_daily_schedule():
    client1 = Client("Alice", "13800138000", "alice@example.com")
    pet = Animal("Mimi", "Cat", owner_id=client1.id)
    clinic = Clinic()
    clinic.add_client(client1)
    clinic.add_animal(pet)
    appt = Appointment("2026-10-10", "in-clinic", client1.id, pet.id)
    clinic.create_appointment(appt)
    daily = clinic.get_daily_schedule("2026-10-10")
    assert len(daily) == 1
