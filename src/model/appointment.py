class Appointment:
    _id_counter = 1
    def __init__(self, date, service_type, client_id, pet_id):
        self.id = Appointment._id_counter
        Appointment._id_counter += 1
        self.date = date
        self.service_type = service_type
        self.client_id = client_id
        self.pet_id = pet_id
