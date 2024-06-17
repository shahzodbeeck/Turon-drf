from rest_framework import serializers

from .models import Years, Month, Day, TypeDay


class TypeDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeDay
        fields = '__all__'


class DaySerializer(serializers.ModelSerializer):
    type_day = TypeDaySerializer(many=True, read_only=True)

    class Meta:
        model = Day
        fields = '__all__'


class MonthSerializer(serializers.ModelSerializer):
    days = DaySerializer(many=True, read_only=True)

    class Meta:
        model = Month
        fields = '__all__'


class YearsSerializer(serializers.ModelSerializer):
    months = MonthSerializer(many=True, read_only=True)

    class Meta:
        model = Years
        fields = '__all__'
