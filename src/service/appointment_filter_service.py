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
            if appt.service_type == appt_type:
                filtered.append(appt)
        return filtered
        
    def filter_by_date(self, target_date: str):
        """US5: Filter appointments by appointment date"""
        filtered = []
        for appt in self.appointments:
            if appt.date == target_date:
                filtered.append(appt)
        return filtered
