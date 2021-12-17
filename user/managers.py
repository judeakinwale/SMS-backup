# from django.db import models
from django.contrib.auth.models import BaseUserManager
from user import models

# Create your managers here.


class UserManager(BaseUserManager):
    """user manager for the custom user model"""

    def create_user(self, email, password=None, **kwargs):
        """create and save a new user"""
        if not email:
            raise ValueError('Users must have a valid email address')
        user = self.model(email=self.normalize_email(email), **kwargs)
        if password is None:
            try:
                password = user.last_name.lower()
            except Exception as e:
                raise ValueError('Users has no last_name')
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staff(self, email, password, **kwargs):
        """create and save a new staff"""
        user = self.create_user(email, password, **kwargs)
        user.is_staff = True
        user.save(using=self._db)
        models.Staff.objects.create(user=user)
        return user

    def create_superuser(self, email, password, **kwargs):
        """create and save a new superuser"""
        user = self.create_user(email, password, **kwargs)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        models.Staff.objects.create(user=user)
        return user
