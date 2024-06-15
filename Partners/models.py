from django.db import models

class Partners(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='partners/')
    url = models.CharField(max_length=255)
