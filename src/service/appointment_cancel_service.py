from src.model.appointment import Appointment

class AppointmentCancelService:
    def __init__(self):
        self.appointments = []

    def add_appointment(self, appt: Appointment):
        # 增加一个status标记，默认active
        appt.status = "active"
        self.appointments.append(appt)

    def cancel_appointment_by_id(self, appt_id: int):
        """US7: Cancel appointment by appointment id"""
        for appt in self.appointments:
            if appt.id == appt_id:
                appt.status = "cancelled"
                return True
        return False

    def get_all_active_appointments(self):
        """Return only active appointments"""
        return [appt for appt in self.appointments if appt.status == "active"]

    def get_all_cancelled_appointments(self):
        """Return only cancelled appointments"""
        return [appt for appt in self.appointments if appt.status == "cancelled"]