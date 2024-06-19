from Teachers.views import *
from .models import Room, TimeTableDay, DailyTable, Flow, TimeList,Students


def calculate_teacher_salary():
    teachers = Teacher.objects.all()
    today = datetime.datetime.today()
    year = Years.objects.get(year=today.year)
    month = Month.objects.get(month_number=today.month, years_id=year.id)
    working_days = Day.objects.filter(month_id=month.id, type_id=1).count()

    for teacher in teachers:
        if teacher.daily_table:
            lesson_count = len(teacher.daily_table.all())
            salary_percentage = teacher.salary_percentage
            calc_salary = (lesson_count / 20) * teacher.teacher_salary_type.salary
            percentage_result = (calc_salary * salary_percentage) / 100

            salary = TeacherSalary.objects.filter(teacher_id=teacher.id, month=month.id).first()
            if salary and salary.worked_days:
                overall = (calc_salary + percentage_result) * (salary.worked_days / working_days)
                salary.salary = round(overall)
                salary.save()
            else:
                overall = calc_salary + percentage_result
                TeacherSalary.objects.create(teacher_id=teacher.id, salary=round(overall), month=month.id)
        else:
            TeacherSalary.objects.filter(teacher_id=teacher.id, month=month.id).update(salary=0)


def check_teacher_timetable(teacher_id, day_id, lesson_time_id, room_id, subject_id, class_id, lesson_id):
    teacher = Teacher.objects.filter(id=teacher_id).first()
    if teacher and teacher.daily_table.exists():
        for daily_table in teacher.daily_table.all():
            if daily_table.day_id == int(day_id) and daily_table.lesson_time.id == int(lesson_time_id):
                if not lesson_id:
                    return {"text": 'bu voxta darsi teacherni', "color": "red"}
                else:
                    filter_lesson = DailyTable.objects.filter(id=lesson_id).first()
                    if filter_lesson and filter_lesson.teacher_id == int(teacher_id):
                        return check_room_timetable(teacher_id, day_id, lesson_time_id, room_id, subject_id, class_id,
                                                    lesson_id)
                    else:
                        return {"text": 'bu voxta darsi teacherni', "color": "red"}
        return check_room_timetable(teacher_id, day_id, lesson_time_id, room_id, subject_id, class_id, lesson_id)
    else:
        return check_room_timetable(teacher_id, day_id, lesson_time_id, room_id, subject_id, class_id, lesson_id)


def check_room_timetable(teacher_id, day_id, lesson_time_id, room_id, subject_id, class_id, lesson_id):
    room = Room.objects.filter(id=room_id).first()
    if room and room.daily_table.exists():
        for daily_table in room.daily_table.all():
            if daily_table.day_id == int(day_id) and daily_table.lesson_time.id == int(lesson_time_id):
                if not lesson_id:
                    return {"text": 'bu voxta xona zanet', "color": "red"}
                else:
                    filter_lesson = DailyTable.objects.filter(id=lesson_id).first()
                    if filter_lesson and filter_lesson.room_id == int(room_id):
                        return update_old_time_table(teacher_id, day_id, lesson_time_id, room_id, subject_id, class_id,
                                                     lesson_id)
                    else:
                        return {"text": 'bu voxta xona zanet', "color": "red"}
        if not lesson_id:
            return add_new_daily_table(teacher_id, day_id, lesson_time_id, room_id, subject_id, class_id, lesson_id)
        else:
            return update_old_time_table(teacher_id, day_id, lesson_time_id, room_id, subject_id, class_id, lesson_id)
    else:
        if not lesson_id:
            return add_new_daily_table(teacher_id, day_id, lesson_time_id, room_id, subject_id, class_id, lesson_id)
        else:
            return update_old_time_table(teacher_id, day_id, lesson_time_id, room_id, subject_id, class_id, lesson_id)


def add_new_daily_table(teacher_id, day_id, lesson_time_id, room_id, subject_id, class_id, lesson_id):
    day = TimeTableDay.objects.filter(id=day_id).first()
    add = DailyTable(teacher_id=teacher_id, subject_id=subject_id, room_id=room_id, class_id=class_id,
                     lesson_time_id=lesson_time_id, day_id=day_id)
    add.save()
    day.daily_table.add(add)
    calculate_teacher_salary()
    return {"text": 'darslik qowildi', "color": "green"}


def update_old_time_table(teacher_id, day_id, lesson_time_id, room_id, subject_id, class_id, lesson_id):
    DailyTable.objects.filter(id=lesson_id).update(
        room_id=room_id,
        subject_id=subject_id,
        teacher_id=teacher_id
    )
    calculate_teacher_salary()
    return {"text": 'darslik yangilandi', "color": "green"}


def flow_student_table_information():
    days = TimeTableDay.objects.all()
    times = TimeList.objects.order_by('id').all()
    day_list = []
    for day in days:
        info = {
            "day_id": day.id,
            "day_name": day.name,
            "lessons": []
        }
        for time in times:
            les = {
                "status": False,
                "time_id": time.id,
                "time_count": time.lesson_count,
                "start": time.start,
                "end": time.end
            }
            info["lessons"].append(les)
            for item in day.daily_table.filter(flow_lesson=True):
                for lesson in info["lessons"]:
                    if lesson["time_id"] == item.lesson_time.id and item.day_id == info["day_id"]:
                        room = Room.objects.filter(id=item.room_id).first()
                        flow = Flow.objects.filter(id=item.flow_id).first()
                        if item.lesson_time.id == les["time_id"]:
                            if flow and room:
                                les.update({
                                    "status": True,
                                    "flow_name": flow.name,
                                    "flow_id": flow.id,
                                    "room_id": room.id,
                                    "room_name": room.name,
                                    "lesson_id": item.id
                                })
                            elif not flow and room:
                                les.update({
                                    "status": True,
                                    "flow_name": None,
                                    "flow_id": None,
                                    "room_id": room.id,
                                    "room_name": room.name,
                                    "lesson_id": item.id
                                })
                            elif not room and flow:
                                les.update({
                                    "status": True,
                                    "flow_name": flow.name,
                                    "flow_id": flow.id,
                                    "room_id": None,
                                    "room_name": None,
                                    "lesson_id": item.id
                                })
        day_list.append(info)
    return day_list


def check_teacher_for_flow_timetable(flow_id, day_id, room_id, lesson_time_id, lesson_id):
    flow = Flow.objects.filter(id=flow_id).first()
    teacher = Teacher.objects.filter(id=flow.teacher_id).first()
    if teacher and teacher.daily_table.exists():
        for daily_table in teacher.daily_table.all():
            if daily_table.day_id == int(day_id) and daily_table.lesson_time.id == int(lesson_time_id):
                if not lesson_id:
                    return {"text": 'bu voxta darsi teacherni', "color": "red"}
                else:
                    filter_lesson = DailyTable.objects.filter(id=lesson_id).first()
                    if filter_lesson and filter_lesson.teacher_id == int(teacher.id):
                        return check_students_for_flow_timetable(flow_id, day_id, room_id, lesson_time_id, lesson_id)
                    else:
                        return {"text": 'bu voxta darsi teacherni', "color": "red"}
        return check_students_for_flow_timetable(flow_id, day_id, room_id, lesson_time_id, lesson_id)
    else:
        return check_students_for_flow_timetable(flow_id, day_id, room_id, lesson_time_id, lesson_id)


def check_students_for_flow_timetable(flow_id, day_id, room_id, lesson_time_id, lesson_id):
    flow = Flow.objects.filter(id=flow_id).first()
    status = True
    filter_time = TimeList.objects.filter(id=lesson_time_id).first()
    for student in flow.students.all():
        student_f = Students.objects.filter(id=student.id).first()
        for classs in student_f.classes.all():
            for daily_table in classs.daily_table.all():
                if classs.class_number <= 4:
                    if filter_time.start == "13:10":
                        return {"text": 'bu kicik sinf abedda boladi', "color": "red"}
                    else:
                        if daily_table.lesson_time.id == int(lesson_time_id) and daily_table.day_id == int(day_id):
                            if not lesson_id:
                                return {"text": f'{classs.class_number} {classs.color} sinfi darsi bor', "color": "red"}
                            else:
                                filter_lesson = DailyTable.objects.filter(id=lesson_id).first()
                                if filter_lesson and filter_lesson.flow_id == int(flow_id):
                                    return check_flow_room_timetable(flow_id, day_id, room_id, lesson_time_id,
                                                                     lesson_id)
                                else:
                                    return {"text": f'{classs.class_number} {classs.color} sinfi darsi bor',
                                            "color": "red"}
                else:
                    if filter_time.start == "12:15":
                        return {"text": 'bu sinfda yuqori sinf abedda boladi', "color": "red"}
                    else:
                        if daily_table.lesson_time.id == int(lesson_time_id) and daily_table.day_id == int(day_id):
                            if not lesson_id:
                                return {"text": f'{classs.class_number} {classs.color} sinfi darsi bor', "color": "red"}
                            else:
                                filter_lesson = DailyTable.objects.filter(id=lesson_id).first()
                                if filter_lesson and filter_lesson.flow_id == int(flow_id):
                                    return check_flow_room_timetable(flow_id, day_id, room_id, lesson_time_id,
                                                                     lesson_id)
                                else:
                                    return {"text": f'{classs.class_number} {classs.color} sinfi darsi bor',
                                            "color": "red"}
    return check_flow_room_timetable(flow_id, day_id, room_id, lesson_time_id, lesson_id)


def check_flow_room_timetable(flow_id, day_id, room_id, lesson_time_id, lesson_id):
    room = Room.objects.filter(id=room_id).first()
    if room and room.daily_table.exists():
        for daily_table in room.daily_table.all():
            if daily_table.day_id == int(day_id) and daily_table.lesson_time.id == int(lesson_time_id):
                if not lesson_id:
                    return {"text": 'xona zanet', "color": "red"}
                else:
                    filter_lesson = DailyTable.objects.filter(id=lesson_id).first()
                    if filter_lesson and filter_lesson.room_id == int(room_id):
                        return update_old_flow_timetable(day_id, lesson_time_id, room_id, lesson_id, flow_id)
                    else:
                        return {"text": 'bu voxtda xona zanet', "color": "red"}
    if not lesson_id:
        return add_flow_timetable(flow_id, day_id, room_id, lesson_time_id, lesson_id)
    else:
        return update_old_flow_timetable(day_id, lesson_time_id, room_id, lesson_id, flow_id)


def add_flow_timetable(flow_id, day_id, room_id, lesson_time_id, lesson_id):
    day = TimeTableDay.objects.filter(id=day_id).first()
    add = DailyTable(flow_id=flow_id, day_id=day_id, lesson_time_id=lesson_time_id, room_id=room_id, flow_lesson=True)
    add.save()
    day.daily_table.add(add)
    calculate_teacher_salary()
    return {"text": 'darslik qowildi', "color": "green"}


def update_old_flow_timetable(flow_id, day_id, room_id, lesson_time_id, lesson_id):
    DailyTable.objects.filter(id=lesson_id).update(
        room_id=room_id,
        flow_id=flow_id
    )
    calculate_teacher_salary()
    return {"text": 'darslik yangilandi', "color": "green"}


def lesson_table_list():
    lesson_list = []
    days = TimeTableDay.objects.all()
    rooms = Room.objects.all()
    times = TimeList.objects.all()
    for day in days:
        day_info = {
            "day_name": day.name,
            "rooms": []
        }
        for room in rooms:
            room_info = {
                "room_name": room.name,
                "lessons": []
            }
            for time in times:
                les = {
                    "status": False,
                    "time_id": time.id,
                    "time_count": time.lesson_count,
                    "start": time.start,
                    "end": time.end
                }
                room_info["lessons"].append(les)
                for item in room.daily_table.filter(day_id=day.id):
                    for lesson in room_info["lessons"]:
                        if lesson["time_id"] == item.lesson_time.id:
                            if item.flow_lesson:
                                subject = Subjects.objects.filter(id=item.flow.subject_id).first()
                                teacher = Teacher.objects.filter(id=item.flow.teacher_id).first()
                                les.update({
                                    "lesson_type": "flow",
                                    "status": True,
                                    "teacher_id": teacher.id,
                                    "teacher_name": f'{teacher.user.name} {teacher.user.surname}',
                                    "subject_id": subject.id,
                                    "subject_name": subject.name,
                                    "lesson_id": item.id,
                                    "flow_name": item.flow.name,
                                    "flow_id": item.flow.id,
                                    "class_id": None
                                })
                            else:
                                room = Room.objects.filter(id=item.room_id).first()
                                teacher = Teacher.objects.filter(id=item.teacher_id).first()
                                subject = Subjects.objects.filter(id=item.subject_id).first()
                                if not room and subject and item.teacher_id:
                                    les.update({
                                        "lesson_type": "simple",
                                        "status": True,
                                        "teacher_id": item.teacher_id,
                                        "teacher_name": f'{teacher.user.name} {teacher.user.surname}',
                                        "subject_id": item.subject_id,
                                        "subject_name": subject.name,
                                        "lesson_id": item.id,
                                        "flow_name": None,
                                        "flow_id": None,
                                        "class_id": item.class_id
                                    })
                                elif not item.teacher_id and subject and room:
                                    les.update({
                                        "lesson_type": "simple",
                                        "status": True,
                                        "room_id": item.room_id,
                                        "room_name": room.name,
                                        "teacher_id": None,
                                        "teacher_name": None,
                                        "subject_id": item.subject_id,
                                        "subject_name": subject.name,
                                        "lesson_id": item.id,
                                        "flow_name": None,
                                        "flow_id": None,
                                        "class_id": item.class_id
                                    })
                                elif not subject and room and item.teacher_id:
                                    les.update({
                                        "lesson_type": "simple",
                                        "status": True,
                                        "room_id": item.room_id,
                                        "room_name": room.name,
                                        "teacher_id": item.teacher_id,
                                        "teacher_name": f'{teacher.user.name} {teacher.user.surname}',
                                        "subject_id": None,
                                        "subject_name": None,
                                        "lesson_id": item.id,
                                        "flow_name": None,
                                        "flow_id": None,
                                        "class_id": item.class_id
                                    })
                                elif not room and not item.teacher_id:
                                    les.update({
                                        "lesson_type": "simple",
                                        "status": True,
                                        "room_id": None,
                                        "room_name": None,
                                        "teacher_id": None,
                                        "teacher_name": None,
                                        "subject_id": item.subject_id,
                                        "subject_name": subject.name,
                                        "lesson_id": item.id,
                                        "flow_name": None,
                                        "flow_id": None,
                                        "class_id": item.class_id
                                    })
                                elif not room and not subject:
                                    les.update({
                                        "lesson_type": "simple",
                                        "status": True,
                                        "room_id": None,
                                        "room_name": None,
                                        "teacher_id": item.teacher_id,
                                        "teacher_name": f'{teacher.user.name} {teacher.user.surname}',
                                        "subject_id": None,
                                        "subject_name": None,
                                        "lesson_id": item.id,
                                        "flow_name": None,
                                        "flow_id": None,
                                        "class_id": item.class_id
                                    })
                                elif not item.teacher_id and not subject:
                                    les.update({
                                        "lesson_type": "simple",
                                        "status": True,
                                        "room_id": item.room_id,
                                        "room_name": room.name,
                                        "teacher_id": None,
                                        "teacher_name": None,
                                        "subject_id": None,
                                        "subject_name": None,
                                        "lesson_id": item.id,
                                        "flow_name": None,
                                        "flow_id": None,
                                        "class_id": item.class_id
                                    })
                                elif item.teacher_id and subject and room:
                                    les.update({
                                        "lesson_type": "simple",
                                        "status": True,
                                        "room_id": item.room_id,
                                        "room_name": room.name,
                                        "teacher_id": item.teacher_id,
                                        "teacher_name": f'{teacher.user.name} {teacher.user.surname}',
                                        "subject_id": item.subject_id,
                                        "subject_name": subject.name,
                                        "lesson_id": item.id,
                                        "flow_name": None,
                                        "flow_id": None,
                                        "class_id": item.class_id
                                    })
            day_info["rooms"].append(room_info)
        lesson_list.append(day_info)
    return lesson_list
