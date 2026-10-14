from src.model.client import Client
from src.model.animal import Animal
from src.model.appointment import Appointment
from src.service.appointment_filter_service import AppointmentFilterService
from src.service.appointment_search_service import AppointmentSearchService


class Clinic:
    def __init__(self):
        self.clients = []
        self.animals = []
        self.appointments = []
        self.filter_service = AppointmentFilterService()
        self.search_service = AppointmentSearchService()

    def add_client(self, client: Client):
        self.clients.append(client)

    def add_animal(self, animal: Animal):
        self.animals.append(animal)

    def create_appointment(self, appt: Appointment):
        self.appointments.append(appt)
        self.filter_service.add_appointment(appt)
        self.search_service.add_appointment(appt)

    def get_all_appointments(self):
        return self.appointments

    def cancel_appointment(self, appt_id):
        self.appointments = [a for a in self.appointments if a.id != appt_id]

    # US5：按日期筛选预约
    def filter_appointments_by_date(self, target_date):
        return self.filter_service.filter_by_date(target_date)

    # US6：根据宠物ID搜索预约
    def search_appointment_by_animal(self, animal_id):
        return self.search_service.search_by_animal_id(animal_id)

    # US7 获取当日日程
    def get_daily_schedule(self, date_str):
        return self.filter_appointments_by_date(date_str)