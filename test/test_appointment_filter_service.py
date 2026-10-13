from src.service.appointment_filter_service import AppointmentFilterService
from src.model.appointment import Appointment

def test_filter_appointment_by_type():
    filter_service = AppointmentFilterService()
    appt1 = Appointment("2026-10-05", "consultation", client_id=1, pet_id=1)
    appt2 = Appointment("2026-10-06", "vaccination", client_id=2, pet_id=2)
    appt3 = Appointment("2026-10-07", "consultation", client_id=3, pet_id=3)
    filter_service.add_appointment(appt1)
    filter_service.add_appointment(appt2)
    filter_service.add_appointment(appt3)
    # filter consultation type
    result = filter_service.filter_by_type("consultation")
    assert len(result) == 2