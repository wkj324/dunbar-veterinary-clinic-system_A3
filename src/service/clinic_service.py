from src.model.appointment import Appointment
from src.model.client import Client
from src.model.animal import Animal
from datetime import datetime

class ClinicService:
    def __init__(self):
        self.appointments = []

    def create_appointment(self, client: Client, animal: Animal, appointment_time: datetime, service: str):
        new_app = Appointment(client, animal, appointment_time, service)
        self.appointments.append(new_app)
        return new_app

    def get_all_appointments(self):
        return self.appointments
