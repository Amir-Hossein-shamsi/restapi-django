from typing import Any
from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser,PermissionsMixin


class CoreUserManager(BaseUserManager):
    """Create Base User Manager for Objects of User model """

    def create_user(self,email:str,password:str,**kwargs):
        """Create and Save new User objects"""
        if email is None:
            raise ValueError("For create new User, email field is requirement")
        user=self.model(email=self.normalize_email(email),**kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user
    

    def create_superuser(self,email,password,**extra_field):
        """Create Super User """
        user=self.create_user(email=email,password=password,**extra_field)
        user.is_superuser=True
        user.is_staff=True
        user.save(using=self._db)

        return user





class User(AbstractBaseUser,PermissionsMixin):
    email=models.EmailField(max_length=255,unique=True)
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)

    objects=CoreUserManager()


    USERNAME_FIELD='email'

