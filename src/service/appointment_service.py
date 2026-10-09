from src.model.appointment import Appointment

class AppointmentService:
    def __init__(self):
        self.appointment_list = []

    def add_appointment(self, appointment):
        self.appointment_list.append(appointment)

    def get_appointment_by_id(self, appointment_id):
        for apt in self.appointment_list:
            if apt.appointment_id == appointment_id:
                return apt
        return None
