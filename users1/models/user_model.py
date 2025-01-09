#models/user_model.py
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from .base_model import BaseModel

class UserManager(BaseUserManager):#add
    def create_user(self, email, username,password=None,**kwargs):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')

        email = self.normalize_email(email)
        user = self.model(email=email,username=username,**kwargs)#create user instance
        user.set_password(password)#sets user passwords and hashing security
        user.save(using=self._db)#save user instance in a specified db
        return user
    def create_superuser(self,email,username,password=None,**kwargs):
        kwargs.setdefault('is_staff',True)
        kwargs.setdefault('is_superuser',True)
        
        if not kwargs.get("is_staff"):
            raise ValueError("Superuser must have is_staff=True")
        return self.create_user(email,username,password,**kwargs)
        if not kwargs.get("is_superuser"):
            raise ValueError("Superuser must have is_superuser=True")
    
class User(AbstractUser,BaseModel):
    email = models.EmailField(unique=True)
    PROFILE_LOGO = models.ImageField(upload_to='profile_logos/',null=True,blank=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']
    objects = UserManager()

    @property
    def logo_url(self):
        if self.PROFILE_LOGO:
            return self.PROFILE_LOGO.url
        return None



    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_users',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_users_permissions',
    )
    def __str__(self):
        return self.email