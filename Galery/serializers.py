from rest_framework import serializers

from .models import Galery


class GalerySerializers(serializers.ModelSerializer):
    class Meta:
        model = Galery
        fields = '__all__'