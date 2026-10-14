from src.service.appointment_service import AppointmentService
from src.model.appointment import Appointment

def test_add_and_get_appointment():
    service = AppointmentService()
    apt1 = Appointment("2026-10-10", "Vaccine", 1, 2)
    service.add_appointment(apt1)
    res = service.get_appointment_by_id(apt1.id)
    assert res is not None
    assert res.date == "2026-10-10"
