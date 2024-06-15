from django.conf import settings
from django.db import models

# from Class.models import Class
from Subjects.models import Subjects


class Teacher(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True)
    subject = models.ForeignKey(Subjects, on_delete=models.CASCADE, blank=True, null=True)
    # classs = models.ForeignKey(Class, on_delete=models.CASCADE, blank=True, null=True)
