from django.db import models


# from Class.models import Class

class Subjects(models.Model):
    name = models.CharField(max_length=100)

    # classs = models.ForeignKey(Class, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name
