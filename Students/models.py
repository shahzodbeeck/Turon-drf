from django.conf import settings

from Class.models import *


class Students(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True)
    classs = models.ForeignKey(Class, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class DeletedStudent(models.Model):
    student = models.ForeignKey(Students, on_delete=models.CASCADE)
    reason = models.CharField(max_length=255)


class DeletedStudentForClasses(models.Model):
    student = models.ForeignKey(Students, on_delete=models.CASCADE)
    class_instance = models.ForeignKey(Class, on_delete=models.CASCADE)
    reason = models.CharField(max_length=255)
