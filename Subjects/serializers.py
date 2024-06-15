from rest_framework import serializers
from .models import Subjects

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subjects
        fields = '__all__'