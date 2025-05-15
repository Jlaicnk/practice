from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import RegexValidator

class SysUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, phonenumber=None, avatar=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        if not username:
            raise ValueError('The Username field must be set')

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, phonenumber=phonenumber, avatar=avatar, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, email, password, **extra_fields)

class SysUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="用户名"
    )
    password = models.CharField(
        max_length=128,
        verbose_name="密码"
    )
    avatar = models.ImageField(
        upload_to='avatars/',
        null=True,
        blank=True,
        verbose_name="用户头像"
    )
    email = models.EmailField(
        null=True,
        unique=True,
        verbose_name="用户邮箱"
    )
    phonenumber = models.CharField(
        max_length=11,
        null=True,
        validators=[
            RegexValidator(
                regex=r'^1[3-9]\d{9}$',
                message="手机号格式错误"
            )
        ],
        unique=True,
        verbose_name="手机号码"
    )
    login_date = models.DateField(
        null=True,
        auto_now=True,
        verbose_name="最后登录时间"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="账号状态（启用/禁用）"
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name="是否为管理员"
    )
    is_superuser = models.BooleanField(
        default=False,
        verbose_name="是否为超级管理员"
    )
    created_time = models.DateField(
        null=True,
        auto_now_add=True,
        verbose_name="创建时间"
    )
    updated_time = models.DateTimeField(
        null=True,
        auto_now=True,
        verbose_name="更新时间"
    )
    remarks = models.TextField(
        max_length=500,
        null=True,
        verbose_name="备注"
    )
    preferences = models.JSONField(
        null=True,
        default=list,
        verbose_name="用户偏好（数组）",
        help_text="例如：['dark_mode', 'notifications']"
    )
    graph_data = models.JSONField(
        null=True,
        default=dict,
        verbose_name="用户导入图谱数据（JSON）",
        help_text="自定义 JSON 结构数据"
    )

    objects = SysUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'phonenumber']

    class Meta:
        db_table = 'sys_user'
        verbose_name = "用户"
        verbose_name_plural = "用户管理"
        ordering = ['-created_time']

    def __str__(self):
        return self.username
