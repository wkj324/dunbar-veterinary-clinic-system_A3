from src.service.appointment_search_service import AppointmentSearchService
from src.model.appointment import Appointment
from src.model.animal import Animal

def test_search_appointment_by_pet_name():
    search_service = AppointmentSearchService()
    pet1 = Animal(name="Mimi", species="Cat", owner_id=1)
    pet2 = Animal(name="Doudou", species="Dog", owner_id=2)
    appt1 = Appointment("2026-10-05", "consultation", client_id=1, pet_id=pet1.id)
    appt2 = Appointment("2026-10-06", "vaccination", client_id=2, pet_id=pet2.id)
    search_service.add_appointment(appt1)
    search_service.add_appointment(appt2)
    # search for Mimi
    found = search_service.search_by_pet_name("Mimi", [pet1, pet2])
    assert len(found) == 1
    assert found[0].pet_id == pet1.id