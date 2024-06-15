from rest_framework import serializers
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'first_name', 'last_name', 'password', 'role', 'birth_date', 'image', 'parent_name', 'number', 'email', 'age']
        extra_kwargs = {
            'password': {'write_only': True},  # Ensures password is write-only
        }

    def create(self, validated_data):
        # Custom implementation for creating a user
        user = CustomUser.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        # Custom implementation for updating a user
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)  # Hash password
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance
