from src.model.client import Client
from src.model.animal import Animal
from src.model.appointment import Appointment

class Clinic:
    def __init__(self):
        self.clients = []
        self.animals = []
        self.appointments = []

    def add_client(self, client: Client):
        self.clients.append(client)

    def add_animal(self, animal: Animal):
        self.animals.append(animal)

    def create_appointment(self, appt: Appointment):
        self.appointments.append(appt)

    def get_all_appointments(self):
        return self.appointments

    def cancel_appointment(self, appt_id):
        self.appointments = [a for a in self.appointments if a.id != appt_id]

    def get_daily_schedule(self, date_str):
        return [a for a in self.appointments if a.date == date_str]
