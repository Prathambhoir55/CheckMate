from rest_framework import serializers
from .models import *
from company.serializers import HRGetSerializer
import numpy as np
import cv2
import base64
from .utils import *

class BlackFlagPostSerializer(serializers.ModelSerializer):
    hr = serializers.IntegerField(read_only=True)
    emp = serializers.IntegerField(read_only=True)
    phone = serializers.IntegerField(write_only = True)
    image = serializers.CharField(write_only=True)
    image_embeddings = serializers.CharField(read_only=True)

    class Meta:
        model = BlackFlag
        fields = ['image', 'phone', 'image_embeddings', 'hr', 'emp']

    def create(self, validated_data, user):
        hr = HR.objects.get(user=user)
        phone = validated_data.pop('phone')
        emp = Employee.objects.get(user__phone_no = phone)
        obj = BlackFlag.objects.create(hr=hr, emp=emp, **validated_data)
        emp.is_blackflag = True
        emp.save()
        validated_data['hr'] = hr.user.name
        return validated_data, obj


class BlackFlagListSerializer(serializers.ModelSerializer):
    hr = HRGetSerializer()

    class Meta:
        model = BlackFlag
        fields = ['image_embeddings', 'hr', 'emp']


class ReasonSerializer(serializers.ModelSerializer):
    flag = BlackFlagPostSerializer()

    class Meta:
        model = Reason
        fields = ['flag', 'text']

    def create(self, validated_data, user):
        phone = validated_data['flag']['phone']
        try:
            obj = BlackFlag.objects.get(emp__user__phone_no = phone)
        except:
            blackflags = BlackFlag.objects.all()

            encodings_list = []
            for item in blackflags:
                output = item.image_embeddings.split(',')
                encodings_list.append([float(n) for n in output])

            encoded_data = validated_data['flag'].pop('image').split(',')[1]
            nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            encodings = calculate_encodings(image)

            boolean_list = compare_faces(encodings_list, encodings)

            if (True in boolean_list):
                index = boolean_list.index(True)
                obj = blackflags[index]
            else:
                encodings =  [str(value) for value in encodings]
                encodings_string = ','.join(encodings)
                validated_data['flag']['image_embeddings'] = encodings_string
                _, obj = BlackFlagPostSerializer().create(validated_data['flag'], user)
        Reason.objects.create(flag = obj, text = validated_data['text'])
        return validated_data


class BlackFlagCheckSerializer(serializers.ModelSerializer):
    phone = serializers.IntegerField(write_only = True)
    image = serializers.CharField(write_only=True)

    class Meta:
        model = BlackFlag
        fields = ['phone', 'image']

    def create(self, validated_data):
        phone = validated_data['phone']
        try:
            obj = BlackFlag.objects.get(emp__user__phone_no = phone)
        except:
            blackflags = BlackFlag.objects.all()

            encodings_list = []
            for item in blackflags:
                output = item.image_embeddings.split(',')
                encodings_list.append([float(n) for n in output])

            encoded_data = validated_data.pop('image').split(',')[1]
            nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            encodings = calculate_encodings(image)

            boolean_list = compare_faces(encodings_list, encodings)

            if (True in boolean_list):
                index = boolean_list.index(True)
                obj = blackflags[index]
            else:
                return {'is_blackflag':False}
        reasons = Reason.objects.filter(flag = obj)
        reasons_list = []
        for item in reasons:
            reasons_list.append(item.text)
        return {'is_blackflag':True, 'reasons':reasons_list}

