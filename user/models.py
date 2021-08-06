from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db.models.fields.related import OneToOneField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from user import managers

# Create your models here.


class User(AbstractBaseUser, PermissionsMixin):
    """Model definition for User."""
    """custom user model that supports using email instead of username"""

    first_name = models.CharField(max_length=250, null=True)
    middle_name = models.CharField(max_length=250, null=True, blank=True)
    last_name = models.CharField(max_length=250, null=True)
    email = models.EmailField(max_length=250, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = managers.UserManager()

    USERNAME_FIELD = 'email'

    class Meta:
        """Meta definition for User."""
        
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        """String representation of User."""
        return self.email


class Staff(models.Model):
    """Model definition for Staff."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'is_staff': True},
    )
    employee_id = models.CharField(max_length=250)
    is_lecturer = models.BooleanField(default=False)
    is_bursar = models.BooleanField(default=False)
    is_head_of_department = models.BooleanField(default=False)

    class Meta:
        """Meta definition for Staff."""

        verbose_name = _("Staff")
        verbose_name_plural = _("Staff")

    def __str__(self):
        """String representation of Staff."""
        return self.employee_id


class Student(models.Model):
    """Model definition for Student."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    matric_no = models.CharField(max_length=250, null=True, blank=True)
    student_id = models.CharField(max_length=250, null=True)

    class Meta:
        """Meta definition for Student."""

        verbose_name = _("Student")
        verbose_name_plural = _("Students")

    def __str__(self):
        """String representation of Student."""
        return self.matric_no if self.matric_no else self.student_id

    
class Biodata(models.Model):
    """Model definition for Biodata."""

    # Model choices
    marriage_choices = (
        ('Single', 'Single'),
        ('Married', 'Married'),
        ('Divorced', 'Divorced'),
        ('Other', 'Other'),
    )
    gender_choices = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    )
    religion_choices = (
        ('Christianity', 'Christianity'),
        ('Islam', 'Islam'),
        ('Other', 'Other'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='biodata'
    )
    marital_status = models.CharField(
        max_length=250,
        choices=marriage_choices,
        default=marriage_choices[-1][-1]
    )
    gender = models.CharField(
        max_length=250,
        choices=gender_choices,
        default=gender_choices[-1][-1]
    )
    religion = models.CharField(
        max_length=250,
        choices=religion_choices,
        default=religion_choices[-1][-1]
    )
    birthday = models.DateField(auto_now=False, auto_now_add=False, null=True)
    nationality = models.CharField(max_length=250, null=True, blank=True)
    state_of_origin = models.CharField(max_length=250, null=True)
    local_govt = models.CharField(max_length=250, null=True)
    permanent_address = models.CharField(max_length=250, null=True)
    address = models.CharField(max_length=250, null=True, blank=True)
    phone_no_1 = models.CharField(max_length=20, null=True)
    phone_no_2 = models.CharField(max_length=20, null=True, blank=True)
    profile_picture = models.ImageField(blank=True, null=True, upload_to='images/profile_pictures/')

    class Meta:
        """Meta definition for Biodata."""

        verbose_name = _("Biodata")
        verbose_name_plural = _("Biodata")

    def __str__(self):
        """String representation of Biodata."""
        if self.user.first_name and self.user.last_name:
            return f"{self.user.last_name} {self.user.first_name}"
        else:
            return self.user.email


class AcademicData(models.Model):
    """Model definition for AcademicData."""

    student = models.OneToOneField(
        Student,
        on_delete=models.CASCADE,
        related_name='academic_data'
    )
    programme = models.CharField(max_length=250, null=True)
    started = models.DateTimeField(null=True)
    ended = models.DateTimeField(null=True, blank=True)
    qualification = models.CharField(max_length=250, null=True, blank=True)

    class Meta:
        """Meta definition for AcademicData."""

        verbose_name = _("AcademicData")
        verbose_name_plural = _("AcademicData")

    def __str__(self):
        """String representation of AcademicData."""
        if self.student.matric_no:
            return self.student.matric_no 
        else:
            return self.student.student_id


class AcademicHistory(models.Model):
    """Model definition for AcademicHistory."""

     # TODO: Add choices for qualification_earned

    biodata = models.ForeignKey(
        Biodata,
        on_delete=models.CASCADE,
        related_name='academic_history',
    )
    institution = models.CharField(max_length=250, null=True)
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)
    qualification_earned = models.CharField(max_length=250, null=True)

    class Meta:
        """Meta definition for AcademicHistory."""

        verbose_name = _("AcademicHistory")
        verbose_name_plural = _("AcademicHistory")

    def __str__(self):
        """String representation of AcademicHistory."""
        return self.biodata


class HealthData(models.Model):
    """Model definition for HealthData."""

    biodata = models.OneToOneField(
        Biodata,
        on_delete=models.CASCADE,
        related_name='health_data',
    )
    blood_group = models.CharField(max_length=300, default='')
    genotype = models.CharField(max_length=300, default='')
    allergies = models.TextField(null=True, blank=True)
    diabetes = models.BooleanField(default=False)
    STIs = models.TextField(null=True, blank=False)
    heart_disease = models.TextField(null=True, blank=True)
    disabilities = models.TextField(null=True, blank=True)
    respiratory_problems = models.TextField(null=True, blank=True)

    class Meta:
        """Meta definition for HealthData."""

        verbose_name = _("HealthData")
        verbose_name_plural = _("HealthData")

    def __str__(self):
        """String representation of HealthData."""
        return self.biodata


class FamilyData(models.Model):
    """Model definition for FamilyData."""

    biodata = models.OneToOneField(
        Biodata,
        on_delete=models.CASCADE,
        related_name='family_data',
    )
    next_of_kin_full_name = models.CharField(max_length=250, null=True)
    next_of_kin_phone_no_1 = models.CharField(max_length=250, null=True)
    next_of_kin_phone_no_2 = models.CharField(max_length=250, null=True)
    next_of_kin_address = models.CharField(max_length=250, null=True)
    guardian_full_name = models.CharField(max_length=250, null=True)
    guardian_phone_no_1 = models.CharField(max_length=250, null=True)
    guardian_phone_no_2 = models.CharField(max_length=250, null=True)
    guardian_address = models.CharField(max_length=250, null=True)

    class Meta:
        """Meta definition for FamilyData."""

        verbose_name = _("FamilyData")
        verbose_name_plural = _("FamilyData")

    def __str__(self):
        """String representation of FamilyData."""
        return self.biodata


