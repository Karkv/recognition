from rest_framework import serializers
from . models import voicerec

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model=voicerec
        fields='__all__'