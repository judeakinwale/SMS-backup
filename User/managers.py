from django.db import models
from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):

    def create_user(self, email, password, some_data):

        if not email:
            raise ValueError('Email is required!')

        if not password:
            raise ValueError('Password is required!')

        user = self.model(
            email=self.normalize_email(email),
            first_name=some_data.get('first_name'),
            last_name=some_data.get('last_name'),
            middle_name=some_data.get('middle_name')
        )

        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, email, password):

        some_data = {}

        if not password:
            raise TypeError('SuperUsers must have password!')

        user = self.create_user(email, password, some_data)
        user.admin = True
        user.is_IT = True
        user.is_staff = True
        user.save()

        return user