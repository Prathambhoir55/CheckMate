from rest_framework import serializers
from .models import *
from accounts.models import *
from accounts.serializers import  UserRegisterSerializer

class HRRegisterSerializer(serializers.ModelSerializer):
    user = UserRegisterSerializer()

    class Meta:
        model = HR
        fields = ['user']

    def validate(self, attrs):
        attrs = attrs.get('user')
        return attrs

    def create(self, validated_data):
        validated_data['is_active'] = True
        user = User.objects.create_user(**validated_data)
        hr, created = HR.objects.get_or_create(user = user)
        return user
    
class EmployeeRegisterSerializer(serializers.ModelSerializer):
    user = UserRegisterSerializer()

    class Meta:
        model = Employee
        fields = ['user', 'photo']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_data['is_active'] = True
        user = User.objects.create_user(**user_data)
        obj, created = Employee.objects.get_or_create(user = user, **validated_data)
        return user
    

class HRGetSerializer(serializers.ModelSerializer):
    user = UserRegisterSerializer()
    class Meta:
        model = HR
        fields = '__all__'


class EmployeeGetSerializer(serializers.ModelSerializer):
    user = UserRegisterSerializer()
    # phone_no = serializers.CharField(write_only=True)

    class Meta:
        model = Employee
        fields = ['id','user','arrival_time', 'leaving_time', 'hr', 'aadhar_card', 'pan_card', 'is_verified', 'photo']
    
    def update(self,validated_data,instance):
        instance.name = validated_data['name'] 
        instance.phone_no = validated_data['phone_no']
        if instance.password != validated_data['password']:
            instance.set_password(validated_data['password'])
        instance.save()
        return instance
    

class EmployeePutSerializer(serializers.ModelSerializer):
    # phone_no = serializers.CharField(write_only=True)
    # hr = serializers.IntegerField(read_only=True)
    user = UserRegisterSerializer()
    class Meta:
        model = Employee
        fields = ['hr','arrival_time', 'leaving_time','aadhar_card', 'pan_card', 'is_verified', 'photo','user']

    def update(self,validated_data, hr):
        instance = Employee.objects.get(user__phone_no = validated_data['phone_no'])
        instance.hr = hr
        instance.save()
        return instance
    
