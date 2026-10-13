from src.model.appointment import Appointment

class AppointmentFilterService:
    def __init__(self):
        self.appointments = []

    def add_appointment(self, appt: Appointment):
        self.appointments.append(appt)

    def filter_by_type(self, appt_type: str):
        """US6: Filter appointments by type (consultation / vaccination)"""
        filtered = []
        for appt in self.appointments:
            if appt.type == appt_type:
                filtered.append(appt)
        return filtered