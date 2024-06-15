from rest_framework import serializers

from .models import Partners


class PartnersSerializers(serializers.ModelSerializer):
    class Meta:
        model = Partners
        fields = '__all__'
