from src.model.appointment import Appointment

class AppointmentSearchService:
    def __init__(self):
        self.appointments = []

    def add_appointment(self, appt: Appointment):
        self.appointments.append(appt)

    def search_by_pet_name(self, pet_name: str, pet_list):
        """US5: Search all appointments by pet name"""
        result = []
        for appt in self.appointments:
            # find pet matching pet_id
            for pet in pet_list:
                if pet.id == appt.pet_id and pet.name == pet_name:
                    result.append(appt)
        return result

    def search_by_animal_id(self, animal_id):
        """US6: Search appointments by animal id"""
        filtered = []
        for appt in self.appointments:
            if appt.pet_id == animal_id:
                filtered.append(appt)
        return filtered