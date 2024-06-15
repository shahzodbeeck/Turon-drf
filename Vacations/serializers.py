from rest_framework import serializers

from .models import TypeInfo, Info, Vacation, Requests


class TypeInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeInfo
        fields = '__all__'


class InfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Info
        fields = '__all__'


class VacationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacation
        fields = '__all__'


class RequestsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requests
        fields = '__all__'
