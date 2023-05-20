from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.authtoken.models import Token
from .serializers import *
from rest_framework.response import Response
from rest_framework import status,permissions


# Create your views here.
class BlackFlagListAPI(ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = BlackFlagListSerializer
    queryset = BlackFlag.objects.all()


class BlackFlagPostAPI(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ReasonSerializer

    def post(self, request):
        data = request.data
        user = request.user
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception= True)
        valid_data = serializer.create(serializer.validated_data, user)
        return Response({"message":"Success", "data":valid_data}, status=status.HTTP_201_CREATED)


class BlackFlagCheckAPI(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BlackFlagCheckSerializer

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception= True)
        valid_data = serializer.create(serializer.validated_data)
        return Response({"message":"Success", "data":valid_data}, status=status.HTTP_201_CREATED)
