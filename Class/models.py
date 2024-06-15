from django.db import models

from Teachers.models import Teacher


class ClassType(models.Model):
    class_number = models.IntegerField()
    color = models.CharField(max_length=255)
    price = models.CharField(max_length=255)


class Class(models.Model):
    type = models.ForeignKey("ClassType", on_delete=models.CASCADE, blank=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, blank=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    # language_type = models.ForeignKey('Language', on_delete=models.CASCADE)
