from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from Users.models import CustomUser as User
from Vacations.models import TypeInfo, Info
from turon.permission import IsAdminOrReadOnly
from .models import TimeTableDay, TimeList, DailyTable, Class, Subjects, Room, Teacher, Flow
from .serializers import TimeTableDaySerializer, TimeListSerializer, DailyTableSerializer
from .utils import check_teacher_timetable, check_teacher_for_flow_timetable, lesson_table_list, \
    flow_student_table_information, calculate_teacher_salary


class TimeTableDayViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)

    queryset = TimeTableDay.objects.all()
    serializer_class = TimeTableDaySerializer


class TimeListViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)

    queryset = TimeList.objects.all()
    serializer_class = TimeListSerializer


class DailyTableViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)

    queryset = DailyTable.objects.all()
    serializer_class = DailyTableSerializer


class CreateTimetableAPIView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)

    def get(self, request, class_id):
        user = get_object_or_404(User, id=1)
        classs = get_object_or_404(Class, id=class_id)
        about_us = get_object_or_404(TypeInfo, id=1)
        news = get_object_or_404(TypeInfo, id=2)
        jobs = get_object_or_404(TypeInfo, id=3)
        about = Info.objects.filter(type_id=about_us.id).order_by('id').first()
        about_id = about.id if about else 0
        subjects = Subjects.objects.all()
        rooms = Room.objects.all()
        teachers = Teacher.objects.all()
        days = TimeTableDay.objects.all()
        times = TimeList.objects.order_by('id').all()
        classes = Class.objects.filter(deleted_classes=None).all()

        new_days = []
        for day in days:
            info = {
                "day_id": day.id,
                "name": day.name,
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
                for item in day.daily_table.filter(class_id=classs.id):
                    for lessons in info["lessons"]:
                        if lessons["time_id"] == item.lesson_time.id:
                            room = item.room
                            teacher = item.teacher
                            subject = item.subject
                            if item.lesson_time.id == les["time_id"]:
                                if not room and subject and item.teacher_id:
                                    les.update({
                                        "status": True,
                                        "teacher_id": item.teacher_id,
                                        "teacher_name": f'{teacher.user.name} {teacher.user.surname}',
                                        "subject_id": item.subject_id,
                                        "subject_name": subject.name,
                                        "lesson_id": item.id
                                    })
                                elif not item.teacher_id and subject and room:
                                    les.update({
                                        "status": True,
                                        "room_id": item.room_id,
                                        "room_name": room.name,
                                        "teacher_id": None,
                                        "teacher_name": None,
                                        "subject_id": item.subject_id,
                                        "subject_name": subject.name,
                                        "lesson_id": item.id
                                    })
                                elif not subject and room and item.teacher_id:
                                    les.update({
                                        "status": True,
                                        "room_id": item.room_id,
                                        "room_name": room.name,
                                        "teacher_id": item.teacher_id,
                                        "teacher_name": f'{teacher.user.name} {teacher.user.surname}',
                                        "subject_id": None,
                                        "subject_name": None,
                                        "lesson_id": item.id
                                    })
                                elif not room and not item.teacher_id:
                                    les.update({
                                        "status": True,
                                        "room_id": None,
                                        "room_name": None,
                                        "teacher_id": None,
                                        "teacher_name": None,
                                        "subject_id": item.subject_id,
                                        "subject_name": subject.name,
                                        "lesson_id": item.id
                                    })
                                elif not room and not subject:
                                    les.update({
                                        "status": True,
                                        "room_id": None,
                                        "room_name": None,
                                        "teacher_id": item.teacher_id,
                                        "teacher_name": f'{teacher.user.name} {teacher.user.surname}',
                                        "subject_id": None,
                                        "subject_name": None,
                                        "lesson_id": item.id
                                    })
                                elif not item.teacher_id and not subject:
                                    les.update({
                                        "status": True,
                                        "room_id": item.room_id,
                                        "room_name": room.name,
                                        "teacher_id": None,
                                        "teacher_name": None,
                                        "subject_id": None,
                                        "subject_name": None,
                                        "lesson_id": item.id
                                    })
                                elif item.teacher_id and subject and room:
                                    les.update({
                                        "status": True,
                                        "room_id": item.room_id,
                                        "room_name": room.name,
                                        "teacher_id": item.teacher_id,
                                        "teacher_name": f'{teacher.user.name} {teacher.user.surname}',
                                        "subject_id": item.subject_id,
                                        "subject_name": subject.name,
                                        "lesson_id": item.id
                                    })
            new_days.append(info)
        return Response({
            "about_us": about_us,
            "news": news,
            "jobs": jobs,
            "about_id": about_id,
            "user": user,
            "rooms": rooms,
            "subjects": subjects,
            "teachers": teachers,
            "days": days,
            "times": times,
            "classs": classs,
            "new_days": new_days,
            "classes": classes
        })


class TimetablesAPIView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)

    def get(self, request):
        user = get_object_or_404(User, id=1)
        about_us = get_object_or_404(TypeInfo, id=1)
        news = get_object_or_404(TypeInfo, id=2)
        jobs = get_object_or_404(TypeInfo, id=3)
        about = Info.objects.filter(type_id=about_us.id).order_by('id').first()
        about_id = about.id if about else 0
        subjects = Subjects.objects.all()
        rooms = Room.objects.all()
        teachers = Teacher.objects.all()
        days = TimeTableDay.objects.all()
        times = TimeList.objects.order_by('id').all()
        classes = Class.objects.filter(deleted_classes=None).all()
        classes_new_days_list = []

        for classs in classes:
            classes_new_days = {
                "class_id": classs.id,
                "new_days": []
            }
            for day in days:
                info = {
                    "day_id": day.id,
                    "name": day.name,
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
                    for item in day.daily_table.filter(class_id=classs.id):
                        for lessons in info["lessons"]:
                            if lessons["time_id"] == item.lesson_time.id:
                                room = item.room
                                teacher = item.teacher
                                subject = item.subject
                                if item.lesson_time.id == les["time_id"]:
                                    if not room and subject and item.teacher_id:
                                        les.update({
                                            "status": True,
                                            "teacher_id": item.teacher_id,
                                            "teacher_name": f'{teacher.user.name} {teacher.user.surname}',
                                            "subject_id": item.subject_id,
                                            "subject_name": subject.name,
                                            "lesson_id": item.id
                                        })
                                    elif not item.teacher_id and subject and room:
                                        les.update({
                                            "status": True,
                                            "room_id": item.room_id,
                                            "room_name": room.name,
                                            "teacher_id": None,
                                            "teacher_name": None,
                                            "subject_id": item.subject_id,
                                            "subject_name": subject.name,
                                            "lesson_id": item.id
                                        })
                                    elif not subject and room and item.teacher_id:
                                        les.update({
                                            "status": True,
                                            "room_id": item.room_id,
                                            "room_name": room.name,
                                            "teacher_id": item.teacher_id,
                                            "teacher_name": f'{teacher.user.name} {teacher.user.surname}',
                                            "subject_id": None,
                                            "subject_name": None,
                                            "lesson_id": item.id
                                        })
                                    elif not room and not item.teacher_id:
                                        les.update({
                                            "status": True,
                                            "room_id": None,
                                            "room_name": None,
                                            "teacher_id": None,
                                            "teacher_name": None,
                                            "subject_id": item.subject_id,
                                            "subject_name": subject.name,
                                            "lesson_id": item.id
                                        })
                                    elif not room and not subject:
                                        les.update({
                                            "status": True,
                                            "room_id": None,
                                            "room_name": None,
                                            "teacher_id": item.teacher_id,
                                            "teacher_name": f'{teacher.user.name} {teacher.user.surname}',
                                            "subject_id": None,
                                            "subject_name": None,
                                            "lesson_id": item.id
                                        })
                                    elif not item.teacher_id and not subject:
                                        les.update({
                                            "status": True,
                                            "room_id": item.room_id,
                                            "room_name": room.name,
                                            "teacher_id": None,
                                            "teacher_name": None,
                                            "subject_id": None,
                                            "subject_name": None,
                                            "lesson_id": item.id
                                        })
                                    elif item.teacher_id and subject and room:
                                        les.update({
                                            "status": True,
                                            "room_id": item.room_id,
                                            "room_name": room.name,
                                            "teacher_id": item.teacher_id,
                                            "teacher_name": f'{teacher.user.name} {teacher.user.surname}',
                                            "subject_id": item.subject_id,
                                            "subject_name": subject.name,
                                            "lesson_id": item.id
                                        })
                classes_new_days["new_days"].append(info)
            classes_new_days_list.append(classes_new_days)

        return Response({
            "about_us": about_us,
            "news": news,
            "jobs": jobs,
            "about_id": about_id,
            "user": user,
            "rooms": rooms,
            "subjects": subjects,
            "teachers": teachers,
            "days": days,
            "times": times,
            "classes_new_days_list": classes_new_days_list,
            "classes": classes
        })


class CreateTableAPIView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)

    def post(self, request):
        data = request.data["info"]
        response = check_teacher_timetable(
            teacher_id=data.get("teacher_id"),
            day_id=data.get("day_id"),
            lesson_time_id=data.get("lesson_time"),
            room_id=data.get("room_id"),
            subject_id=data.get("subject_id"),
            class_id=data.get("class_id"),
            lesson_id=data.get("lesson_id")
        )
        return Response({"status": response})


class DeleteItemInLessonAPIView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)

    def post(self, request):
        data = request.data["info"]
        time_table_day = get_object_or_404(TimeTableDay, id=data.get("time_table_day_id"))
        lesson_id = data.get("lesson_id")

        if data.get("text") == "room":
            DailyTable.objects.filter(id=lesson_id).update(room_id=None)
        elif data.get("text") == "subject":
            DailyTable.objects.filter(id=lesson_id).update(subject_id=None)
        elif data.get("text") == "teacher":
            DailyTable.objects.filter(id=lesson_id).update(teacher_id=None)
            calculate_teacher_salary()

        daily_table_all_none = DailyTable.objects.filter(
            id=lesson_id,
            subject_id=None,
            room_id=None,
            teacher_id=None
        ).first()

        if daily_table_all_none:
            time_table_day.daily_table.remove(daily_table_all_none)
            daily_table_all_none.delete()
            calculate_teacher_salary()

        return Response({})


class FlowTimetableAPIView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)

    def get(self, request):
        user = get_object_or_404(User, id=1)
        about_us = get_object_or_404(TypeInfo, id=1)
        news = get_object_or_404(TypeInfo, id=2)
        jobs = get_object_or_404(TypeInfo, id=3)
        about = Info.objects.filter(type_id=about_us.id).order_by('id').first()
        about_id = about.id if about else 0
        subjects = Subjects.objects.all()
        rooms = Room.objects.all()
        teachers = Teacher.objects.all()
        days = TimeTableDay.objects.all()
        times = TimeList.objects.order_by('id').all()
        day_list = flow_student_table_information()
        flows = Flow.objects.all()

        return Response({
            "about_us": about_us,
            "news": news,
            "jobs": jobs,
            "about_id": about_id,
            "user": user,
            "rooms": rooms,
            "subjects": subjects,
            "teachers": teachers,
            "days": days,
            "times": times,
            "day_list": day_list,
            "flows": flows
        })


class CreateFlowTimetableAPIView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)

    def post(self, request):
        data = request.data["info"]
        response = check_teacher_for_flow_timetable(
            day_id=data.get("day_id"),
            lesson_time_id=data.get("lesson_time"),
            room_id=data.get("room_id"),
            lesson_id=data.get("lesson_id"),
            flow_id=data.get("flow_id")
        )
        return Response({"status": response})


class DeleteFlowItemInLessonAPIView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)

    def post(self, request):
        data = request.data["info"]
        time_table_day = get_object_or_404(TimeTableDay, id=data.get("time_table_day_id"))
        lesson_id = data.get("lesson_id")

        if data.get("text") == "room":
            DailyTable.objects.filter(id=lesson_id).update(room_id=None)
        elif data.get("text") == "flow":
            DailyTable.objects.filter(id=lesson_id).update(flow_id=None)
            calculate_teacher_salary()

        daily_table_all_none = DailyTable.objects.filter(
            id=lesson_id,
            room_id=None,
            flow_id=None
        ).first()

        if daily_table_all_none:
            time_table_day.daily_table.remove(daily_table_all_none)
            daily_table_all_none.delete()
            calculate_teacher_salary()

        return Response({})


class LessonTableAPIView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)

    def get(self, request):
        user = get_object_or_404(User, id=1)
        about_us = get_object_or_404(TypeInfo, id=1)
        news = get_object_or_404(TypeInfo, id=2)
        jobs = get_object_or_404(TypeInfo, id=3)
        about = Info.objects.filter(type_id=about_us.id).order_by('id').first()
        about_id = about.id if about else 0
        times = TimeList.objects.all()
        lesson_list = lesson_table_list()
        days = TimeTableDay.objects.all()

        return Response({
            "about_us": about_us,
            "news": news,
            "jobs": jobs,
            "about_id": about_id,
            "user": user,
            "times": times,
            "lesson_list": lesson_list,
            "days": days
        })

    def post(self, request):
        data = request.data
        response = check_teacher_timetable(
            teacher_id=data.get('teacher_id'),
            day_id=data.get('day_id'),
            lesson_time_id=data.get('lesson_time_id'),
            room_id=data.get('room_id'),
            subject_id=data.get('subject_id'),
            class_id=data.get('class_id'),
            lesson_id=data.get('lesson_id')
        )
        return Response(response, status=status.HTTP_200_OK)


class CheckTimetableAPIView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)

    def post(self, request):
        data = request.data
        response = check_teacher_timetable(
            teacher_id=data.get('teacher_id'),
            day_id=data.get('day_id'),
            lesson_time_id=data.get('lesson_time_id'),
            room_id=data.get('room_id'),
            subject_id=data.get('subject_id'),
            class_id=data.get('class_id'),
            lesson_id=data.get('lesson_id')
        )
        return Response(response, status=status.HTTP_200_OK)
