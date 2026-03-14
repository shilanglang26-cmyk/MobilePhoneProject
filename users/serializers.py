from rest_framework import serializers
from .models import User, Address
from django.contrib.auth.hashers import make_password  # 密码加密工具


# 用户注册序列化器
class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("id", "username", "phone", "password", "balance")

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


# ✅ 增强版用户序列化器（支持查询+修改+密码修改）
class UserSerializer(serializers.ModelSerializer):
    # 密码字段：只写（不返回给前端，安全）
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ("id", "username", "phone", "password", "balance")
        read_only_fields = ("balance",)  # 余额禁止直接修改

    # 重写更新方法：密码加密存储
    def update(self, instance, validated_data):
        # 如果传入了密码，进行加密
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        # 执行更新
        return super().update(instance, validated_data)


# 地址序列化器
class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"
        read_only_fields = ("user",)
