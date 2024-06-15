from django.db import models


class Job(models.Model):
    name = models.CharField(max_length=255)

    def add(self):
        self.save()

    def __str__(self):
        return self.name
