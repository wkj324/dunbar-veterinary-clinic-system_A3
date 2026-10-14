from src.service.appointment_cancel_service import AppointmentCancelService
from src.model.appointment import Appointment

def test_cancel_appointment_us7():
    # 创建预约
    appt1 = Appointment("2026-10-15", "consultation", client_id=1, pet_id=1)
    appt2 = Appointment("2026-10-16", "vaccination", client_id=2, pet_id=2)

    cancel_service = AppointmentCancelService()
    cancel_service.add_appointment(appt1)
    cancel_service.add_appointment(appt2)

    # 取消appt1
    result = cancel_service.cancel_appointment_by_id(appt1.id)
    assert result is True

    # 校验状态
    assert appt1.status == "cancelled"
    assert appt2.status == "active"

    # 筛选有效预约，只剩下appt2
    active_list = cancel_service.get_all_active_appointments()
    assert len(active_list) == 1
    assert active_list[0].id == appt2.id

    cancelled_list = cancel_service.get_all_cancelled_appointments()
    assert len(cancelled_list) == 1
    assert cancelled_list[0].id == appt1.id

def test_cancel_non_exist_appointment():
    # 测试取消不存在id，返回False
    cancel_service = AppointmentCancelService()
    res = cancel_service.cancel_appointment_by_id(999)
    assert res is False
