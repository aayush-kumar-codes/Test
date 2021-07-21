from django.db import models
from django.utils.translation import ugettext_lazy as _
from .managers import CustomUserManager
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin




# Model of Users

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    username = models.CharField(max_length=100,default=None)
    name = models.CharField(max_length=100,default=None)
    phone_number = models.CharField(blank=True, null=True, max_length=100)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()
    
    is_active = models.BooleanField(default=True,null=True,blank=True)
    is_staff = models.BooleanField(default=False,null=True,blank=True)
    is_superuser = models.BooleanField(default=False,null=True,blank=True)

    def __str__(self):
        if self.email:
            return self.email
        else:
            return ""