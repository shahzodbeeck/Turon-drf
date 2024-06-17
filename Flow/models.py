from django.db import models

from Students.models import Students
from Subjects.models import Subjects
from Teachers.models import Teacher


class Flow(models.Model):
    name = models.CharField(max_length=255)
    subject = models.ForeignKey(Subjects, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    students = models.ManyToManyField(Students,  related_name='flows')







class LanguageType(models.Model):
    name = models.CharField(max_length=100)



