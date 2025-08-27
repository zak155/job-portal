from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
# Create your models here.
class User(AbstractBaseUser,PermissionsMixin):
    email=models.EmailField(unique=True)
    password=models.CharField(max_length=255)
    USERNAME_FIELD="email"
    REQUIRED_FIELDS=[]
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)