from rest_framework import serializers
from shop.models import AvailableMarks


class MarksSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvailableMarks
        fields = ('name', 'is_available')