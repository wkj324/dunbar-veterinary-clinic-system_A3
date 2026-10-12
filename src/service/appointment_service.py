from src.model.appointment import Appointment

class AppointmentService:
    def __init__(self):
        self.appointment_list = []

    def add_appointment(self, appt: Appointment):
        self.appointment_list.append(appt)

    def get_appointment_by_id(self, appointment_id):
        for apt in self.appointment_list:
            if apt.id == appointment_id:
                return apt
        return None

