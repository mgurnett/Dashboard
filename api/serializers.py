from datetime import datetime
from django.utils import timezone
from rest_framework import serializers
from core.models import *
from icecream import ic

# This file's job is to convert a model object which is very complex into a simple form that the responce can send out as json.

class ReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reading
        fields = '__all__'

    def create(self, validated_data):
        # ic(validated_data)

        instance = super().create(validated_data)

        # All this does in update the last time the chain was updated
        chain = Chain.objects.get(id=instance.sensor.chain.id)
        chain.latest_update = timezone.now()
        chain.save()

        if instance.value > instance.sensor.alarm:
            instance.alarm_state = 1
            instance.save()

        return instance 


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'

    def create(self, validated_data):
        # ic(validated_data)

        instance = super().create(validated_data)

        instance.save()

        return instance  
    