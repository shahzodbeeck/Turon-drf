from rest_framework import serializers

from Subjects.serializers import SubjectSerializer, Subjects
from Users.models import CustomUser
from Users.serializers import CustomUserSerializer
from .models import Teacher


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
    user = CustomUserSerializer()
    subject = SubjectSerializer()

    class Meta:
        model = Teacher
        fields = ['id', 'user', 'subject']
