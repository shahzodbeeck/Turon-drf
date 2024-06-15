from django.db import models

from Teachers.models import Teacher


class Room(models.Model):
    name = models.CharField(max_length=255)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    chair_count = models.IntegerField()
    image = models.ImageField(upload_to="images/rooms")

    def __str__(self):
        return self.name
