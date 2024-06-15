from rest_framework import serializers

from Students.models import Students
from Subjects.models import Subjects
from Teachers.models import Teacher
from .models import Flow


class FlowSerializer(serializers.ModelSerializer):
    subject_id = serializers.PrimaryKeyRelatedField(source='subject', queryset=Subjects.objects.all())
    teacher_id = serializers.PrimaryKeyRelatedField(source='teacher', queryset=Teacher.objects.all())
    student_ids = serializers.PrimaryKeyRelatedField(source='students', queryset=Students.objects.all(), many=True)

    class Meta:
        model = Flow
        fields = ('id', 'name', 'subject_id', 'teacher_id', 'student_ids')
