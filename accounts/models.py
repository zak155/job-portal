from django.db import models
from datetime import datetime,timezone
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from .manager import CustomUserManager
from common.models import BaseModel
import uuid
# Create your models here.
class TokenType(models.TextChoices):
    PASSWORD_RESET=("PASSWORD_RESET",)
class User(BaseModel,AbstractBaseUser,PermissionsMixin):
    email=models.EmailField(unique=True)
    password=models.CharField(max_length=255)
    USERNAME_FIELD="email"
    REQUIRED_FIELDS=[]
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)

    objects=CustomUserManager()
class PendingUser(BaseModel):
    email=models.EmailField()
    password=models.CharField(max_length=255)
    verification_code=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    #Timestamp automatically set when the row is created.
    #Used to expire codes after a certain time (so attackers can’t reuse old codes).

    def is_valid(self) -> bool:
        #A helper method that checks if the verification code is still valid.
        #Returns True if within the allowed time window, else False.
        lifespan_in_seconds=20 * 60
        now=datetime.now(timezone.utc)
        #Subtracts the time the user registered (created_at) from current time.
        #Produces a timedelta object.
        timediff=now-self.created_at  
        timediff=timediff.total_seconds()
        if timediff>lifespan_in_seconds:
            return False
        return True

class Token(models.Model):
      id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
      user=models.ForeignKey(User,on_delete=models.CASCADE)
      token=models.CharField(max_length=25)
      token_type = models.CharField(max_length=50,choices=TokenType.choices,default=TokenType.PASSWORD_RESET)  # ✅ default added


      created_at=models.DateTimeField(auto_now_add=True)

      def __str__(self):
          return f"{self.user} {self.token}"
      def is_valid(self) -> bool:
        #A helper method that checks if the verification code is still valid.
        #Returns True if within the allowed time window, else False.
        lifespan_in_seconds=20 * 60
        now=datetime.now(timezone.utc)
        #Subtracts the time the user registered (created_at) from current time.
        #Produces a timedelta object.
        timediff=now-self.created_at  
        timediff=timediff.total_seconds()
        if timediff>lifespan_in_seconds:
            return False
        return True
      def reset_user_password(self,raw_password:str):
          self.user:User
          self.user.set_password(raw_password)
          self.user.save()