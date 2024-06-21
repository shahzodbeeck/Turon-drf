# serializers.py
from rest_framework import serializers

from Class.models import Class
from Class.serializers import ClassSerializer
from Users.models import CustomUser
from Users.serializers import CustomUserSerializer
from .models import Students,DeletedStudent,PdfContract

class RegisterStudentSerializer(serializers.Serializer):
    user_id = serializers.CharField()
    classs = serializers.CharField()

    def create(self, validated_data):
        class_id = validated_data.pop('classs')
        try:
            class_instance = Class.objects.get(id=class_id)
        except Class.DoesNotExist:
            raise serializers.ValidationError(f"Class with id {class_id} does not exist.")

        user_id = validated_data.pop('user_id')
        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError(f"User with id {user_id} does not exist.")

        student, created = Students.objects.get_or_create(user=user, defaults={'classs': class_instance})
        if not created:
            student.classs = class_instance
            student.save()

        return student


class StudentSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    classs = ClassSerializer()

    class Meta:
        model = Students
        fields = ['id', 'user', 'classs']
class DeletedStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeletedStudent
        fields = '__all__'
class PdfContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = PdfContract
        fields = '__all__'