from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from user import managers
from academics import models as acmodels

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
    employee_id = models.CharField(max_length=250, null=True)
    programme = models.ForeignKey(acmodels.Programme, on_delete=models.DO_NOTHING, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_lecturer = models.BooleanField(default=False)
    is_bursar = models.BooleanField(default=False)
    is_IT = models.BooleanField(default=False)
    is_head_of_department = models.BooleanField(default=False)
    is_dean_of_faculty = models.BooleanField(default=False)

    class Meta:
        """Meta definition for Staff."""

        verbose_name = _("Staff")
        verbose_name_plural = _("Staff")

    def __str__(self):
        """String representation of Staff."""
        return f"{self.employee_id or self.user.email}"


class Student(models.Model):
    """Model definition for Student."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    matric_no = models.CharField(max_length=250, null=True, blank=True)
    student_id = models.CharField(max_length=250, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        """Meta definition for Student."""

        verbose_name = _("Student")
        verbose_name_plural = _("Students")

    def __str__(self):
        """String representation of Student."""
        # return f"{self.matric_no if self.matric_no else self.student_id}"
        return f"{self.matric_no or self.student_id or self.user.email}"

    
class Biodata(models.Model):
    """Model definition for Biodata."""


    # Definitions for model choices
    class MarriageChoices(models.TextChoices):
        SINGLE = 'Single', _('Single')
        MARRIED = 'Married', _('Married')
        DIVORCED = 'Divorced', _('Divorced')
        OTHER = 'Other', _('Other')


    class GenderChoices(models.TextChoices):
        MALE = 'Male', _('Male')
        FEMALE = 'Female', _('Female')
        OTHER = 'Other', _('Other')


    class ReligionChoices(models.TextChoices):
        CHRISTIANITY = 'Christianity', _('Christianity')
        ISLAM = 'Islam', _('Islam')
        OTHER = 'Other', _('Other')


    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='biodata',
    )
    marital_status = models.CharField(
        max_length=250,
        choices=MarriageChoices.choices,
        default=MarriageChoices.OTHER,
    )
    gender = models.CharField(
        max_length=250,
        choices=GenderChoices.choices,
        default=GenderChoices.OTHER,
    )
    religion = models.CharField(
        max_length=250,
        choices=ReligionChoices.choices,
        default=ReligionChoices.OTHER,
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


    # Definitions for model choices
    class QualificationChoices(models.TextChoices):
        OTHER = 'Other', _('Other') 


    student = models.OneToOneField(
        Student,
        on_delete=models.CASCADE,
        related_name='academic_data'
    )
    programme = models.ForeignKey(acmodels.Programme, on_delete=models.CASCADE, null=True, blank=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True, blank=True)
    qualification = models.CharField(
        max_length=250,
        choices=QualificationChoices.choices,
        null=True,
        default=QualificationChoices.OTHER,
    )

    class Meta:
        """Meta definition for AcademicData."""

        verbose_name = _("AcademicData")
        verbose_name_plural = _("AcademicData")

    def __str__(self):
        """String representation of AcademicData."""
        return f"{self.student.matric_no if self.student.matric_no else self.student.student_id}"


class CourseRegistration(models.Model):
    """Model definition for CourseRegistration."""

    # TODO:
    # convert session and semester to foreignkeys or datetime choices

    course = models.ForeignKey(acmodels.Course, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    session = models.CharField(max_length=250, null=True, blank=True)
    semester = models.CharField(max_length=250, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_completed = models.BooleanField(default=False)
    is_passed = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta:
        """Meta definition for CourseRegistration."""

        verbose_name = _('CourseRegistration')
        verbose_name_plural = _('CourseRegistrations')

    def __str__(self):
        """String representation of CourseRegistration."""
        return f"{self.course.name} - registration"


class AcademicHistory(models.Model):
    """Model definition for AcademicHistory."""

    # Definitions for model choices
    class QualificationChoices(models.TextChoices):
        OTHER = 'Other', _('Other') 

    biodata = models.ForeignKey(
        Biodata,
        on_delete=models.CASCADE,
        related_name='academic_history',
    )
    institution = models.CharField(max_length=250, null=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    qualification_earned = models.CharField(
        max_length=250,
        choices=QualificationChoices.choices,
        null=True,
        default=QualificationChoices.OTHER,
    )

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
    blood_group = models.CharField(max_length=300, null=True, blank=True)
    genotype = models.CharField(max_length=300, null=True, blank=True)
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
