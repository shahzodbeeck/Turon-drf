from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    role = models.CharField(max_length=150, verbose_name='role', null=True)
    birth_date = models.DateTimeField(verbose_name="birth_date", null=True)
    image = models.ImageField(upload_to='photos/%Y/%m/%d', verbose_name='photo', blank=True)
    parent_name = models.CharField(blank=True, null=True)
    number = models.CharField(max_length=150, verbose_name='number', null=True)
    email = models.EmailField(null=True)
    age = models.CharField(max_length=150, verbose_name='age', null=True)