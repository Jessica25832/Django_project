from django.core import validators
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager
from shortuuidfield import ShortUUIDField

class UserManager(BaseUserManager):
    def _create_user(self, telephone,username,password,email,**kwargs):
        if not telephone:
            raise ValueError('The given telephone must be set')
        if not username:
            raise ValueError('The given username must be set')
        if not password:
            raise ValueError('The given password must be set')
        user = self.model(telephone=telephone,username=username, email=email,**kwargs)
        user.set_password(password)
        user.save()
        return user
    # 创建普通用户
    def create_user(self, telephone,username, password, email=None, **kwargs):
        kwargs['is_staff']=False
        kwargs['is_superuser']=False
        return self._create_user(telephone,username, password,email,**kwargs)
    #创建超级用户
    def create_superuser(self, telephone,username, password,email=None,**kwargs):
        kwargs['is_staff'] = True
        kwargs['is_superuser'] = True
        return self._create_user(telephone,username,password,email,**kwargs)


from django.contrib.auth.models import AbstractUser
class User(AbstractBaseUser,PermissionsMixin):
    #主键不使用自增 使用 uuid/shortuuid
    #pip install django-shortuuidfield
    uid = ShortUUIDField(primary_key=True)
    telephone = models.CharField(max_length=11,unique=True,validators=[validators.RegexValidator(r'1[3-9]\d{9}',message="请输入正确的手机号")])
    email = models.EmailField(unique=True,null=True)
    username = models.CharField(max_length=100,unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    data_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'telephone'
    REQUIRED_FIELDS = ['username']

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def get_black_list(self):
        return self.objects.filter(is_active=False)


