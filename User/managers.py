from django.db import models
from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):

    def create_user(self, email, password, **kwargs):

        if not email:
            raise ValueError('Email is required!')

        if not password:
            raise ValueError('Password is required!')

        user = self.model(email=self.normalize_email(email), **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, email, password):

        if not password:
            raise TypeError('SuperUsers must have password!')

        user = self.create_user(email, password)
        user.admin = True
        user.is_IT = True
        user.is_staff = True
        user.save(using=self._db)
        return user