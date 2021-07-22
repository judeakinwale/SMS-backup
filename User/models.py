import uuid
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from .managers import UserManager


# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=250, null=True)
    last_name = models.CharField(max_length=250, null=True)
    middle_name = models.CharField(max_length=250, null=True)
    email = models.EmailField(max_length=250, unique=True)
    matric_no = models.CharField(max_length=250, default='')
    is_IT = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    is_Lecturer = models.BooleanField(default=False)
    is_Student = models.BooleanField(default=False)
    is_Bursar = models.BooleanField(default=False)
    is_HOD = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email


    @property
    def is_superuser(self):
        return self.admin

    # class Meta:
    #     db_table = "login"


class BioData(models.Model):
    marriage_choices = (
        ('Single', 'Single'),
        ('Married', 'Married'),
        ('Divorced', 'Divorced')
    )
    gender_choices = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other')
    )
    religion_choices = (
        ('Christianity', 'Christianity'),
        ('Islam', 'Islam'),
        ('Other', 'Other')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='biodata')
    email = models.EmailField(max_length=250, unique=True)
    first_name = models.CharField(max_length=250, null=True)
    last_name = models.CharField(max_length=250, null=True)
    middle_name = models.CharField(max_length=250, null=True, blank=True)
    matric_no = models.CharField(max_length=250, default='')
    marital_status = models.CharField(max_length=250, default='', choices=marriage_choices)
    gender = models.CharField(max_length=250, default='', choices=gender_choices)
    religion = models.CharField(max_length=250, default='', choices=religion_choices)
    birthday = models.DateField(auto_now=False, auto_now_add=False, null=True)
    nationality = models.CharField(max_length=250, blank=True, null=True)
    state_of_origin = models.CharField(max_length=250, default='')
    local_govt = models.CharField(max_length=250, default='')
    permanent_address = models.CharField(max_length=250, default='')
    phone1 = models.CharField(max_length=20, default='')
    phone2 = models.CharField(max_length=20, default='')
    profile_picture = models.ImageField(blank=True, null=True, upload_to='media/')

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    # class Meta:
    #     db_table = "biodata"


class AcademicData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='academic_data')
    faculty = models.CharField(max_length=300, default='')
    department = models.CharField(max_length=300, default='')
    programme = models.CharField(max_length=300, default='')

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
    
    # class Meta:
    #     db_table = "academic_data"


class HealthData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='health_data')
    blood_group = models.CharField(max_length=300, default='')
    genotype = models.CharField(max_length=300, default='')
    allergies = models.TextField(blank=True)
    diabetes = models.BooleanField(default=False)
    STIs = models.TextField(blank=False)
    heart_disease = models.TextField(blank=True)
    disabilities = models.TextField(blank=True)
    respiratory_problems = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    # class Meta:
    #     db_table = "health_data"


class FamilyData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='family_data')
    next_of_kin = models.CharField(max_length=300, default='')
    next_of_kin_phone1 = models.CharField(max_length=300, default='')
    next_of_kin_phone2 = models.CharField(max_length=300, default='')
    next_of_kin_address = models.CharField(max_length=300, default='')
    guardian = models.CharField(max_length=300, default='')
    guardian_phone1 = models.CharField(max_length=300, default='')
    guardian_phone2 = models.CharField(max_length=300, default='')
    guardian_address = models.CharField(max_length=300, default='')
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    # class Meta:
    #     db_table = "family_data"


