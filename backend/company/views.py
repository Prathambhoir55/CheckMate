from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.authtoken.models import Token
from .serializers import *
from rest_framework.response import Response
from rest_framework import status,permissions
# Create your views here.

class HRRegisterAPI(GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = HRRegisterSerializer
    
    def post(self,request,*args,**kwargs):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception = True)
        user = serializer.save()

        token = Token.objects.create(user=user)
        return Response({"message":"Success", "token":token.key, "user": serializer.validated_data}, status=status.HTTP_201_CREATED)
  
class EmployeeRegisterAPI(GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = EmployeeRegisterSerializer
    
    def post(self,request,*args,**kwargs):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception = True)
        user = serializer.save()
        token = Token.objects.create(user=user)
        return Response({"message":"Success", "token":token.key, "employee":serializer.validated_data}, status=status.HTTP_201_CREATED)


class EmployeeListAPI(ListAPIView):
    serializer_class = EmployeeGetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        hr = HR.objects.get(user = self.request.user)
        queryset = Employee.objects.filter(hr = hr)
        return queryset


class EmployeeDropDownAPI(ListAPIView):
    serializer_class = EmployeeGetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Employee.objects.filter(user__company = self.request.user.company).exclude(user=self.request.user)
        return queryset


class AllEmployeeListAPI(ListAPIView):
    serializer_class = EmployeeGetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Employee.objects.all()
        return queryset


class HRGetAPI(GenericAPIView):
    serializer_class = HRGetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            user = HR.objects.get(user = request.user)
            # hr = user.hr_set()
            serializer = self.serializer_class(user)
        except:
            return Response("User not found", status= status.HTTP_404_NOT_FOUND)
        return Response(serializer.data)

    def put(self,request,*args,**kwargs):
        user = HR.objects.get(user=request.user)
        data = request.data
        serializer = self.serializer_class(data=data)
        user = serializer.update(request.data, user)
        return Response(request.data, status = status.HTTP_200_OK)


class EmpGetAPI(GenericAPIView):
    serializer_class = EmployeeGetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            user = Employee.objects.get(id = request.user.id)
            serializer = self.serializer_class(user)
        except:
            return Response("User not found", status= status.HTTP_404_NOT_FOUND)
        return Response(serializer.data)

class EmpPutAPI(GenericAPIView):
    serializer_class = EmployeePutSerializer
    permission_classes = [permissions.IsAuthenticated]

    def put(self,request,*args,**kwargs):
        hr = HR.objects.get(user=request.user)
        data = request.data 
        serializer = self.serializer_class(hr, data=request.data,partial=True)
        # serializer = self.serializer_class(data=data, many=True)
        if serializer.is_valid():
            validated_data = serializer.update(serializer.validated_data, hr)
            return Response({"message":"Success", "data":request.data}, status = status.HTTP_200_OK)
        return Response({"message":"data not valid"}, status= status.HTTP_400_BAD_REQUEST)


class HRGetEmployee(GenericAPIView):
    serializer_class = EmployeeGetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self, request, pk):
        # try:
        user = Employee.objects.get(user__phone_no = pk)
        serializer = self.serializer_class(user)
        return Response(serializer.data)