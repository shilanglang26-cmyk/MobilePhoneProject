from django.http import HttpResponse, JsonResponse
from rest_framework import status, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .model import Address
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer, LogoutSerializer, AddressSerializer


class RegisterView(APIView):
    """用户注册（支持手机号/邮箱）"""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return JsonResponse({
                "code": status.HTTP_200_OK,
                "msg": "注册成功",
                "data": UserSerializer(user).data
            }, status=status.HTTP_200_OK)
        return JsonResponse(
            {
                "code": status.HTTP_404_NOT_FOUND,
                "msg": "注册失败",
                "data": serializer.errors
            },
            status=status.HTTP_200_OK
        )


class LoginView(APIView):
    """用户登录（手机号+用户名+密码）"""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            refresh = RefreshToken.for_user(user)
            return JsonResponse({
                "code": status.HTTP_200_OK,
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "data": UserSerializer(user).data,
                "msg": "登陆成功",
            })
        return JsonResponse(
            {
                "code": status.HTTP_404_NOT_FOUND,
                "msg": "登陆失败",
                "data": serializer.errors
            },
            status=status.HTTP_200_OK
        )


class LogoutView(APIView):
    """用户退出（用户ID）"""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            refresh = RefreshToken.for_user(user)
            return JsonResponse(
                {
                    "code": status.HTTP_200_OK,
                    "msg": "退出成功",
                    "data": UserSerializer(user).data
                },
                status=status.HTTP_200_OK
            )
        return JsonResponse(
            {
                "code": status.HTTP_404_NOT_FOUND,
                "msg": "退出失败",
                "data": serializer.errors
            },
            status=status.HTTP_200_OK
        )


class TokenRefreshView(APIView):
    """用户登录（手机号/用户名+密码）"""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": UserSerializer(user).data
            })
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


class AddressViewSet(viewsets.ModelViewSet):
    """
    地址的增删改查视图集
    list: 获取当前用户的所有地址
    retrieve: 获取单个地址详情
    create: 添加新地址
    update: 修改地址（全量更新）
    partial_update: 部分更新地址
    destroy: 删除地址
    """
    # 指定序列化器
    serializer_class = AddressSerializer
    # 权限：必须登录才能操作
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        重写查询集：只返回当前登录用户的地址
        确保用户只能操作自己的地址
        """
        return Address.objects.filter(user=self.request.user).order_by('-created_at')

    def create(self, request, *args, **kwargs):
        """重写创建方法，添加成功提示"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return JsonResponse({
            'code': status.HTTP_200_OK,
            'msg': '地址添加成功',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        """重写更新方法，添加成功提示"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return JsonResponse({
            'code': status.HTTP_200_OK,
            'msg': '地址修改成功',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        """重写删除方法，添加成功提示"""
        instance = self.get_object()
        self.perform_destroy(instance)
        return JsonResponse({
            'code': status.HTTP_200_OK,
            'msg': '地址删除成功'
        }, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def set_default(self, request, pk=None):
        """
        自定义动作：设置默认地址
        URL: /addresses/{pk}/set_default/
        """
        address = self.get_object()
        # 将当前用户所有地址设为非默认
        Address.objects.filter(user=request.user, is_default=True).update(is_default=False)
        # 将当前地址设为默认
        address.is_default = True
        address.save()
        return Response({
            'code': status.HTTP_200_OK,
            'msg': '已设为默认地址',
            'data': AddressSerializer(address).data
        })

    @action(detail=False, methods=['get'])
    def default_address(self, request):
        """
        自定义动作：获取当前用户的默认地址
        URL: /addresses/default_address/
        """
        default_addr = Address.objects.filter(user=request.user, is_default=True).first()
        if not default_addr:
            return Response({
                'code': status.HTTP_400_BAD_REQUEST,
                'msg': '暂无默认地址'
            }, status=status.HTTP_404_NOT_FOUND)
        return Response({
            'code': 200,
            'data': AddressSerializer(default_addr).data
        })
