from rest_framework import serializers
from .models import *
from company.serializers import HRGetSerializer

class BlackFlagPostSerializer(serializers.ModelSerializer):
    hr = serializers.IntegerField(read_only=True)
    emp = serializers.IntegerField(read_only=True)
    image = serializers.CharField(write_only=True)

    class Meta:
        model = BlackFlag
        fields = ['image', 'image_embeddings', 'hr', 'emp', 'text']

    def create(self, validated_data, hr):
        obj = BlackFlag.objects.create(hr=hr,**validated_data)
        validated_data['hr'] = hr.user.name
        return validated_data, obj


class BlackFlagListSerializer(serializers.ModelSerializer):
    hr = HRGetSerializer()

    class Meta:
        model = BlackFlag
        fields = ['image_embeddings', 'hr', 'emp', 'text']


class ReasonSerializer(serializers.ModelSerializer):
    flag = BlackFlagPostSerializer()

    class Meta:
        model = Reason
        fields = ['flag', 'text']

    def create(self, validated_data, hr):
        _, obj = BlackFlagPostSerializer.create(validated_data['flag'], hr)
        Reason.objects.create(flag = obj, text = validated_data['text'])
        return validated_data
