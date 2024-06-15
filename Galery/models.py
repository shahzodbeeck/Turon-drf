from django.db import models


# Create your models here.
class Galery(models.Model):
    image = models.ImageField(null=False)
