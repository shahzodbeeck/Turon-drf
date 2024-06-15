from django.db import models
from django.utils import timezone


class TypeInfo(models.Model):
    name = models.CharField(max_length=255)

    def add(self):
        self.save()


class Info(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    img = models.CharField(max_length=255)
    type_info = models.ForeignKey(TypeInfo, on_delete=models.CASCADE, related_name='infos')
    date = models.DateTimeField(default=timezone.now)

    def add(self):
        self.save()


class Vacation(models.Model):
    info = models.ForeignKey(Info, on_delete=models.CASCADE, related_name='vacations')
    text = models.TextField()

    def add(self):
        self.save()


class Requests(models.Model):
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    vacation = models.ForeignKey(Vacation, on_delete=models.CASCADE, related_name='requests')
    add_date = models.DateTimeField(default=timezone.now)
    pdf_file = models.CharField(max_length=255)

    def add(self):
        self.save()
