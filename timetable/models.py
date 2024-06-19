from django.db import models
from Subjects.models import Subjects
from Flow.models import Flow
from Rooms.models import Room
from Class.models import Class
from Teachers.models import Teacher
from Students.models import Students
class TimeList(models.Model):
    lesson_count = models.CharField(max_length=255)
    start = models.CharField(max_length=255)
    end = models.CharField(max_length=255)

class TimeTableDay(models.Model):
    name = models.CharField(max_length=255)

class DailyTable(models.Model):
    lesson_time = models.ForeignKey(TimeList, on_delete=models.CASCADE, related_name='daily_times')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='daily_tables')
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='daily_tables')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='daily_tables')
    flow = models.ForeignKey(Flow, on_delete=models.CASCADE, related_name='daily_tables', null=True, blank=True)
    subject = models.ForeignKey(Subjects, on_delete=models.CASCADE, related_name='daily_tables')
    day = models.ForeignKey(TimeTableDay, on_delete=models.CASCADE, related_name='daily_tables')
    flow_lesson = models.BooleanField(default=False)
