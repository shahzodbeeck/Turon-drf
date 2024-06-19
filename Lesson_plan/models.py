from django.db import models

from Calendar.models import Day,Years,Month
from timetable.models import Teacher, TimeList,DailyTable


class LessonPlanDay(models.Model):
    name = models.CharField(max_length=255)
    target = models.TextField()
    main = models.TextField()
    assessment = models.TextField()
    homework = models.TextField()
    day = models.ForeignKey(Day, on_delete=models.CASCADE)
    lesson_time = models.ForeignKey(TimeList, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    def add(self):
        self.save()
