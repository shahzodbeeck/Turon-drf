from rest_framework import serializers

from .models import *


class RegisterTeacherSerializer(serializers.Serializer):
    user_id = serializers.CharField()
    subject_id = serializers.CharField()

    def create(self, validated_data):
        subject_name = validated_data.pop('subject_id')
        try:
            subject = Subjects.objects.get(id=subject_name)
        except Subjects.DoesNotExist:
            raise serializers.ValidationError(f"Subject {subject_name} with the provided name does not exist.")

        username = validated_data.pop('user_id')
        user, created = CustomUser.objects.get_or_create(id=username)
        try:
            teacher = Teacher.objects.get(user=user)
            teacher.subject = subject
            teacher.save()
        except Teacher.DoesNotExist:
            teacher = Teacher.objects.create(user=user, subject=subject)

        return teacher


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'


class TeacherSalaryTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherSalaryType
        fields = '__all__'


class TeacherSalarySerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherSalary
        fields = '__all__'


class TeacherAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherAttendance
        fields = '__all__'


class GivenSalariesInMonthSerializer(serializers.ModelSerializer):
    class Meta:
        model = GivenSalariesInMonth
        fields = '__all__'
