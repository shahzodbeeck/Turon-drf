from rest_framework import serializers
from .models import  Teacher ,Flow,Students,LanguageType,Subjects
from Students.serializers import StudentSerializer



class FlowSerializer(serializers.ModelSerializer):
    students = StudentSerializer(many=True)

    class Meta:
        model = Flow
        fields = '__all__'

class LanguageTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LanguageType
        fields = '__all__'

