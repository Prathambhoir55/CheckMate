from rest_framework.generics import GenericAPIView
from rest_framework.authtoken.models import Token
from .serializers import *
from django.contrib.auth import authenticate,login
from rest_framework.response import Response
from rest_framework import status,permissions

# Create your views here.

class UserRegisterAPI(GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserRegisterSerializer
    
    def post(self,request,*args,**kwargs):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception = True)
        user = serializer.save()
        token = Token.objects.create(user=user)
        return Response({"message":"Success", "token":token.key}, status=status.HTTP_201_CREATED)


class LoginAPI(GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer
	
    def post(self,request,*args,**kwargs ):
        phone_no = request.data.get('phone_no',None)
        password = request.data.get('password',None)
        user = authenticate(phone_no = phone_no, password = password)
        if user :
            login(request,user)
            serializer = self.serializer_class(user)
            token = Token.objects.get(user=user)
            return Response({"message":"Success", "token":token.key},status = status.HTTP_200_OK)
        else:   
            return Response({"message":"Invalid Credentials"},status = status.HTTP_404_NOT_FOUND)

class UserGetAPI(GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            serializer = self.serializer_class(request.user)
        except:
            return Response("User not found", status= status.HTTP_404_NOT_FOUND)
        return Response(serializer.data)

    def put(self,request,*args,**kwargs):
        user = request.user
        data = request.data
        serializer = self.serializer_class(data=data)
        user = serializer.update(request.data, user)
        return Response(request.data, status = status.HTTP_200_OK)

