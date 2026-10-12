from src.model.appointment import Appointment
from src.service.appointment_service import AppointmentService

def test_add_and_get_appointment():
    service = AppointmentService()
    apt1 = Appointment(1, 1, "2026-10-10", "Vaccine")
    service.add_appointment(apt1)
    res = service.get_appointment_by_id(1)
    assert res.appointment_id == 1
    assert res.description == "Vaccine"

def test_appointment_not_found():
    service = AppointmentService()
    res = service.get_appointment_by_id(999)
    assert res is None

def test_cancel_appointment_success():
    service = AppointmentService()
    apt1 = Appointment(1, 1, "2026-10-10", "Vaccine")
    service.add_appointment(apt1)
    result = service.cancel_appointment(1)
    assert result == True
    assert service.get_appointment_by_id(1) is None

def test_cancel_appointment_not_exist():
    service = AppointmentService()
    result = service.cancel_appointment(999)
    assert result == False    
