from datetime import date, datetime

# Sprint1 feature branch: appointment CRUD
class Appointment:
    def __init__(self, appointment_id, client, animal, start_time: datetime, service_type):
        self.appointment_id = appointment_id
        self.client = client
        self.animal = animal
        self.start_time = start_time
        self.service_type = service_type
        self.is_cancelled = False

    def cancel(self):
        self.is_cancelled = True

class InClinicAppointment(Appointment):
    # In-clinic fixed 15 minutes
    duration_min = 15

class FarmVisitAppointment(Appointment):
    def __init__(self, appointment_id, client, animal, start_time: datetime, service_type, duration_min):
        super().__init__(appointment_id, client, animal, start_time, service_type)
        self.duration_min = duration_min


class ClinicService:
    def __init__(self):
        self.appointments = []

def create_appointment(self, client, animal, start_time, service_type):
    # 自动生成id，简单用当前列表长度
    appointment_id = len(self.appointments) + 1
    appointment = InClinicAppointment(appointment_id, client, animal, start_time, service_type)
    self.appointments.append(appointment)
    return appointment


    def cancel_appointment(self, appointment_id):
        for apt in self.appointments:
            if apt.appointment_id == appointment_id and not apt.is_cancelled:
                apt.cancel()
                return True
        return False

    def get_daily_schedule(self, target_date: date):
        daily_list = []
        for apt in self.appointments:
            if apt.start_time.date() == target_date and not apt.is_cancelled:
                daily_list.append(apt)
        return daily_list

    def get_all_appointments(self):
        return self.appointments
