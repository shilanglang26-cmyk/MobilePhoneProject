from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone

from rest_framework import serializers
from .model import User, Address


# 用户基础序列化器（返回用户基本信息）
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'phone', 'email', 'avatar', 'is_active')
        extra_kwargs = {
            "id": {"read_only": True},
            "password": {"write_only": True}
        }


# 注册序列化器（处理用户注册数据验证）
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6, label="密码")
    password_confirm = serializers.CharField(write_only=True, label="确认密码")

    class Meta:
        model = User
        fields = ('id', 'username', 'phone', 'email', 'password', 'password_confirm')
        read_only_fields = ('id',)

    def validate(self, attrs):
        # 验证两次密码一致
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("两次密码输入不一致")
        # 验证手机号格式
        phone = attrs.get('phone')
        if phone:
            # 校验手机号是否为纯数字
            if not phone.isdigit():
                raise serializers.ValidationError({"phone": "手机号必须是纯数字"})
            # 校验手机号是否为11位
            if len(phone) != 11:
                raise serializers.ValidationError({"phone": "手机号必须是11位数字"})
            # 校验手机号是否已存在
            if User.objects.filter(phone=phone).exists():
                raise serializers.ValidationError({"phone": "该手机号已被注册，请更换"})
        return attrs

    def create(self, validated_data):
        # 删除确认密码字段，避免存入数据库
        validated_data.pop('password_confirm')
        # 提取明文密码（后续用于加密）
        raw_password = validated_data.pop('password')
        # 哈希加密密码
        hashed_password = make_password(raw_password)
        # 当前时间YYYY-MM-DD h:m:s格式
        current_time = timezone.now()
        # 创建用户并加密密码
        user = User.objects.create(
            username=validated_data['username'],
            phone=validated_data['phone'],
            email=validated_data.get('email'),
            password=hashed_password,
            date_joined=current_time,
            last_login=current_time,
        )
        return user


# 登录序列化器
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(label="用户名")
    password = serializers.CharField(label="密码", write_only=True)
    phone = serializers.CharField(label="手机号")

    def validate(self, attrs):
        # 根据手机号找到对应的用户
        login_phone = attrs['phone'].strip()
        login_account = attrs['username'].strip()
        if len(login_account) == 11 and login_account.isdigit():
            # 手机号登录
            user = User.objects.get(phone=login_phone)
        else:
            # 用户名登录
            user = User.objects.get(username=login_account)
        # 验证密码（核心：对比明文和哈希密码）
        if not check_password(attrs['password'], user.password):
            raise serializers.ValidationError("用户名/手机号或密码错误")

        # 验证账号状态（适配你的is_active字段）
        if not user.is_active:
            raise serializers.ValidationError("该账号已被禁用")

        # 记录最后登录时间（可选）
        user.last_login = timezone.now()
        user.save(update_fields=['last_login'])
        attrs['user'] = user
        return attrs


# 登陆退出序列化器
class LogoutSerializer(serializers.Serializer):
    id = serializers.CharField(label="用户名ID")

    def validate(self, attrs):
        # 根据手机号找到对应的用户
        logout_id = attrs['id'].strip()
        user = User.objects.get(id=logout_id)
        if not user:
            raise serializers.ValidationError("用户不存在！")
        # 记录最后登录时间
        user.last_login = timezone.now()
        user.save(update_fields=['last_login'])
        attrs['user'] = user
        return attrs


class AddressSerializer(serializers.ModelSerializer):
    """地址序列化器"""
    # 隐藏用户字段，避免前端传入，由后端自动赋值
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Address
        # 排除id和created_at（自动生成），其他字段都参与序列化/反序列化
        exclude = ['id', 'created_at']

    def validate(self, attrs):
        """
        验证逻辑：
        1. 确保手机号是11位
        2. 如果设置为默认地址，将该用户其他地址的is_default设为False
        """
        # 验证手机号
        phone = attrs.get('phone')
        if len(phone) != 11 or not phone.isdigit():
            raise serializers.ValidationError("手机号必须是11位数字")

        # 处理默认地址逻辑
        if attrs.get('is_default'):
            user = self.context['request'].user
            # 将该用户所有地址设为非默认
            Address.objects.filter(user=user, is_default=True).update(is_default=False)

        return attrs