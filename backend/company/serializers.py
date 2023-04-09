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

    class Meta:
        model = Employee
        fields = ['user','arrival_time', 'leaving_time', 'hr', 'aadhar_card', 'pan_card', 'is_verified', 'photo']
    

class EmployeePutSerializer(serializers.ModelSerializer):
    phone_no = serializers.CharField(write_only=True)
    hr = serializers.IntegerField(read_only=True)

    class Meta:
        model = Employee
        fields = ['hr', 'phone_no','arrival_time', 'leaving_time','aadhar_card', 'pan_card', 'is_verified', 'photo']

    def update(self,validated_data, hr):
        instance = Employee.objects.get(user__phone_no = validated_data['phone_no'])
        instance.hr = hr
        instance.save()
        return instance
    

class MyComplaintSerializer(serializers.ModelSerializer):

    class Meta:
        model=Complaint
        fields=['issued_by','issued_for','text','is_resolved','hr']


class HRComplaintSerializer(serializers.ModelSerializer):

    class Meta:
        model=Complaint
        fields=['issued_by','issued_for','text','is_resolved','hr']


class RegisterComplaintSerializer(serializers.ModelSerializer):
    is_resolved = serializers.BooleanField(default=False)
    issued_by = serializers.IntegerField(read_only=True)
    hr = serializers.IntegerField(read_only=True)

    class Meta:
        model=Complaint
        fields=['issued_by','issued_for','text','is_resolved', 'hr']

    def create(self, validated_data, employee):
        employee2 = validated_data.pop('issued_for')
        hr = employee.hr
        complaint = Complaint.objects.create(issued_by = employee, issued_for=employee2, hr=hr, **validated_data)
        validated_data['issued_for'] = employee2.user.name
        validated_data['issued_by'] = employee.user.name
        validated_data['hr'] = hr.user.name
        return validated_data

    
