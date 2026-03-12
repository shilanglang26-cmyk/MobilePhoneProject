from django.db import models

from utils.snowflake import snowflake_generator


class User(models.Model):
    """用户表模型"""
    # 用户ID，雪花ID作为主键，自动生成
    id = models.BigIntegerField(
        primary_key=True,
        default=snowflake_generator.generate_id,  # 注册时自动生成雪花ID
        editable=False,  # 禁止手动编辑
        verbose_name="用户ID（雪花ID）"
    )
    # 用户名
    username = models.CharField(
        max_length=150,
        verbose_name='用户名',
        null=False,
        unique=True
    )
    # 加密密码
    password = models.CharField(
        max_length=128,
        verbose_name='加密密码',
        null=False
    )
    # 手机号（非空，唯一，注释说明MD5加密存储）
    phone = models.CharField(
        max_length=11,
        verbose_name='手机号（MD5加密存储）',
        null=False,
        unique=True
    )
    # 邮箱（可空）
    email = models.EmailField(
        max_length=254,
        verbose_name='邮箱',
        null=True,
        blank=True
    )
    # 用户头像（可空）
    avatar = models.CharField(
        max_length=255,
        verbose_name='用户头像',
        default='',
    )
    # 账号状态（默认1-正常，0-禁用）
    is_active = models.BooleanField(
        verbose_name='账号状态（1-正常，0-禁用）',
        default=True
    )
    # 是否为管理员（默认0-普通用户，1-管理员）
    is_staff = models.BooleanField(
        verbose_name='是否为管理员（0-普通用户，1-管理员）',
        default=False
    )
    # 是否为超级管理员（默认0）
    is_superuser = models.BooleanField(
        verbose_name='是否为超级管理员',
        default=False
    )
    # 注册时间（默认当前时间，非空）
    date_joined = models.DateTimeField(
        verbose_name='注册时间',
        auto_now_add=True,
        null=False
    )
    # 最后登录时间（可空）
    last_login = models.DateTimeField(
        verbose_name='最后登录时间',
        null=True,
        blank=True
    )

    class Meta:
        # 指定数据库表名
        db_table = 'user'
        # 表注释
        verbose_name = '用户表'
        verbose_name_plural = verbose_name
        # 添加联合索引
        indexes = [
            models.Index(fields=['username', 'phone'], name='idx_username_phone'),
        ]


class Address(models.Model):
    """地址表（1:N关联用户）"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="addresses", verbose_name="关联用户")
    receiver = models.CharField(max_length=20, verbose_name="收货人")
    phone = models.CharField(max_length=11, verbose_name="收货电话")
    province = models.CharField(max_length=20, verbose_name="省份")
    city = models.CharField(max_length=20, verbose_name="城市")
    detail_address = models.CharField(max_length=200, verbose_name="详细地址")
    is_default = models.BooleanField(default=False, verbose_name="是否默认地址")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = "收货地址"
        verbose_name_plural = "收货地址"
