from django.conf import settings
from django.db import models

from Class.models import Class


class Students(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True)
    classs = models.ForeignKey(Class, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
