from rest_framework import serializers
from .models import TimeList, TimeTableDay, DailyTable

class TimeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeList
        fields = '__all__'

class TimeTableDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeTableDay
        fields = '__all__'

class DailyTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyTable
        fields = '__all__'
