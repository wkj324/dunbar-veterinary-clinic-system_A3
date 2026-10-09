from src.model.animal import Animal
from src.model.client import Client
from datetime import datetime

class Appointment:
    def __init__(self, client: Client, animal: Animal, appointment_time: datetime, service: str):
        self.client = client
        self.animal = animal
        self.appointment_time = appointment_time
        self.service = service
