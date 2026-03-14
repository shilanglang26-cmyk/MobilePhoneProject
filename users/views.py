from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import User, Address
from .serializers import UserRegisterSerializer, UserSerializer, AddressSerializer
from rest_framework.viewsets import ModelViewSet


# 用户注册
class UserRegisterView(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"code": 200, "msg": "注册成功"})
        return Response({"code": 400, "msg": serializer.errors})


# 用户登录（JWT自带接口，仅继承）
class UserLoginView(TokenObtainPairView):
    pass


# 用户信息修改/删除
class UserManageView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


# 用户地址CRUD
class AddressView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = AddressSerializer

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)