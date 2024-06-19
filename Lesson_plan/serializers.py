from rest_framework import serializers

from .models import *


class LessonPlanDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonPlanDay
        fields = '__all__'
