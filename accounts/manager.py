from django.contrib.auth.base_user import BaseUserManager
class CustomUserManager(BaseUserManager):
    def create_user(self,email,password,**extra_fields):
        if not email:
            raise ValueError("email must be set")
        user=self.model(email=email,**extra_fields)
        user.set_password(password)