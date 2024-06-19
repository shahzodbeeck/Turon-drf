import datetime

from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from turon.permission import IsAdminOrReadOnly
from .models import *
from .serializers import LessonPlanDaySerializer

class LessonPlanDayViewSet(viewsets.ModelViewSet):
    queryset = LessonPlanDay.objects.all()
    serializer_class = LessonPlanDaySerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)


    @action(detail=False, methods=['post'])
    def add_lesson_plan(self, request):
        user = request.user
        teacher = get_object_or_404(Teacher, user=user)
        data = request.data
        lesson_plan = LessonPlanDay(
            name=data["name"],
            target=data["target"],
            main=data["main"],
            assessment=data["assessment"],
            homework=data["homework"],
            day=get_object_or_404(Day, id=data["day_id"]),
            lesson_time=get_object_or_404(TimeList, id=data["lesson_time_id"]),
            teacher=teacher
        )
        lesson_plan.add()
        return Response(status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def change_lesson_plan(self, request):
        data = request.data
        lesson_plan = get_object_or_404(LessonPlanDay, day_id=data["day_id"], lesson_time_id=data["lesson_time_id"])
        lesson_plan.name = data["name"]
        lesson_plan.target = data["target"]
        lesson_plan.main = data["main"]
        lesson_plan.assessment = data["assessment"]
        lesson_plan.homework = data["homework"]
        lesson_plan.save()
        return Response(status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def get_lesson_plan(self, request):
        data = request.data
        lesson_plan = LessonPlanDay.objects.filter(day_id=data["day_id"], lesson_time_id=data["lesson_time_id"]).first()
        if lesson_plan:
            lesson_data = {
                'name': lesson_plan.name,
                'target': lesson_plan.target,
                'assessment': lesson_plan.assessment,
                'main': lesson_plan.main,
                'homework': lesson_plan.homework,
                'status': True
            }
        else:
            lesson_data = {'status': False}
        return Response({'lesson_data': lesson_data})

    @action(detail=True, methods=['get'])
    def filter_day_lesson(self, request, pk=None):
        teacher_id = pk
        date = datetime.today()
        today = date.strftime("%d")
        this_month = date.strftime("%m")
        this_year = date.strftime("%Y")

        year_this = get_object_or_404(Years, year=this_year)
        month_this = get_object_or_404(Month, month_number=this_month)
        day_in_month = Day.objects.filter(month_id=month_this.id, years_id=year_this.id).order_by('id').all()
        day_list = []
        day_table = [
            {'id': 1, 'name': 'Monday'},
            {'id': 2, 'name': 'Tuesday'},
            {'id': 3, 'name': 'Wednesday'},
            {'id': 4, 'name': 'Thursday'},
            {'id': 5, 'name': 'Friday'},
            {'id': 6, 'name': 'Saturday'},
            {'id': 7, 'name': 'Sunday'}
        ]
        for day in day_in_month:
            day_lesson_id = next((days['id'] for days in day_table if days['name'] == day.day_name), None)
            day_lesson_all = DailyTable.objects.filter(day_id=day_lesson_id).order_by('id').all()
            time_list = TimeList.objects.order_by('id').all()
            day_lessons = []

            if day_lesson_all.exists():
                for time in time_list:
                    info_day = {
                        'status': False,
                        'time_id': None,
                        'lesson_status': None
                    }
                    for day_lesson in day_lesson_all:
                        if day_lesson.lesson_time.id == time.id:
                            lesson_plan = LessonPlanDay.objects.filter(day_id=day.id, lesson_time_id=time.id).first()
                            lesson_status = bool(lesson_plan)
                            info_day.update({
                                'status': True,
                                'time_id': day_lesson.lesson_time.id,
                                'lesson_status': lesson_status
                            })
                    if info_day['status']:
                        info = {
                            'name': 'Sinf',
                            'time_id': info_day['time_id'],
                            'lesson_status': info_day['lesson_status']
                        }
                        day_lessons.append(info)
                    else:
                        day_lessons.append({'name': None})
            else:
                day_lessons.extend({'name': None} for _ in time_list)

            day_change_status = int(day.years.year) >= int(this_year) and int(day.month.month_number) >= int(
                this_month) and int(day.day_number) >= int(today)

            day_object = {
                'day_id': day.id,
                'day_number': day.day_number,
                'day_name': day.day_name,
                'day_lessons': day_lessons,
                'day_change_status': day_change_status
            }
            day_list.append(day_object)
        return Response(day_list)
