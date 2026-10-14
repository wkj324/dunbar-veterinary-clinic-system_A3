from src.service.clinic_service import Clinic
from src.model.client import Client
from src.model.animal import Animal
from src.model.appointment import Appointment

if __name__ == "__main__":
    print("===== Dunbar兽医诊所管理系统 演示 =====")
    clinic = Clinic()

    # US1：新增客户
    print("\n--- US1 添加客户 ---")
    c1 = Client("Alice", "13800138000", "alice@test.com")
    clinic.add_client(c1)
    print(f"已创建客户：{c1.name}, ID:{c1.id}")

    # US2：添加宠物，归属客户
    print("\n--- US2 添加宠物 ---")
    pet1 = Animal("Mimi", "Cat", owner_id=c1.id)
    clinic.add_animal(pet1)
    print(f"已创建宠物：{pet1.name}, 所属客户ID:{pet1.owner_id}")

    # US3：创建预约
    print("\n--- US3 创建预约 ---")
    appt1 = Appointment("2026-10-20", "in-clinic", c1.id, pet1.id)
    clinic.create_appointment(appt1)
    print(f"新建预约：日期{appt1.date}")

    # US4：取消预约
    print("\n--- US4 取消预约 ---")
    clinic.cancel_appointment(appt1.id)
    print(f"预约{appt1.id}已执行取消操作")

    # US5：按日期筛选预约
    print("\n--- US5 筛选预约 ---")
    appt2 = Appointment("2026-10-20", "in-clinic", c1.id, pet1.id)
    clinic.create_appointment(appt2)
    result = clinic.filter_appointments_by_date("2026-10-20")
    print(f"2026-10-20预约数量：{len(result)}")

    # US6：搜索宠物对应的预约
    print("\n--- US6 根据宠物ID搜索预约 ---")
    search_result = clinic.search_appointment_by_animal(pet1.id)
    print(f"该宠物的预约总数：{len(search_result)}")

    # US7：查看每日日程
    print("\n--- US7 获取当日日程 ---")
    schedule = clinic.get_daily_schedule("2026-10-20")
    print(f"当日日程列表：{schedule}")

    print("\n==== 全部用户故事功能演示完成 ====")