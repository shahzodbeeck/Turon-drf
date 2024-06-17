from rest_framework import serializers

# from Students.serializers import StudentSerializer
# from Teachers.serializers import TeacherSerializer
from .models import *


class ClassSerializer(serializers.ModelSerializer):
    # students = StudentSerializer(many=True, read_only=True)
    # teacher = TeacherSerializer(many=True, read_only=True)

    # language = serializers.CharField(source='language.name', read_only=True)

    class Meta:
        model = Class
        fields = '__all__'


class ClassTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassType
        fields = '__all__'
