from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from user import managers
from academics import models as acmodels
from . import utils
# from academics import serializers as aserializers

# Create your models here.


class User(AbstractBaseUser, PermissionsMixin):
    """Model definition for User."""
    """custom user model that supports using email instead of username"""

    first_name = models.CharField(max_length=250, null=True)
    middle_name = models.CharField(max_length=250, null=True, blank=True)
    last_name = models.CharField(max_length=250, null=True)
    email = models.EmailField(max_length=250, unique=True)
    specialization = models.ForeignKey(
        acmodels.Specialization,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = managers.UserManager()

    USERNAME_FIELD = 'email'

    class Meta:
        """Meta definition for User."""

        ordering = ['id']
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        """String representation of User."""
        if self.first_name is not None and self.last_name is not None:
            return f"{self.last_name} {self.first_name}"
        else:
            return f"{self.email}"

    # def get_staff(self):
    #     if self.is_staff is True:
    #         try:
    #             staff = Staff.objects.get(user=self)
    #         except Exception:
    #             staff = Staff.objects.create(user=self)
    #         return staff
    #     else:
    #         return None
    
    def get_full_name(self):
        if self.first_name and self.last_name and self.middle_name:
            return f"{self.last_name} {self.first_name} {self.middle_name}"
        elif self.first_name and self.last_name:
            return f"{self.last_name} {self.first_name}"
        else:
            return f"{self.email}"


class Staff(models.Model):
    """Model definition for Staff."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'is_staff': True},
    )
    employee_id = models.CharField(max_length=250, unique=True, null=True)
    specialization = models.ForeignKey(
        acmodels.Specialization,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True
    )
    is_active = models.BooleanField(default=True)
    is_lecturer = models.BooleanField(default=False)
    is_bursar = models.BooleanField(default=False)
    is_IT = models.BooleanField(default=False)
    is_head_of_department = models.BooleanField(default=False)
    is_dean_of_faculty = models.BooleanField(default=False)
    is_course_adviser = models.BooleanField(default=False)

    class Meta:
        """Meta definition for Staff."""

        ordering = ['id']
        verbose_name = _("Staff")
        verbose_name_plural = _("Staff")

    def save(self, *args, **kwargs):
        if self.user.specialization and self.specialization != self.user.specialization:
            self.specialization = self.user.specialization
        super(Staff, self).save(*args, **kwargs)

    def __str__(self):
        """String representation of Staff."""
        return f"{self.employee_id or self.user.email}"

    def department(self):
        try:
            dept = self.specialization.department
            # serialiazer = aserializers.DepartmentSerializer(dept)
            return dept.name
        except Exception:
            return None

    def faculty(self):
        try:
            dept = self.specialization.department
            faculty = dept.faculty
            # serializer = aserializers.FacultySerializer(faculty)
            return faculty.name
        except Exception:
            return None


class Student(models.Model):
    """Model definition for Student."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    matric_no = models.CharField(max_length=250, unique=True, null=True, blank=True)
    student_id = models.CharField(max_length=250, unique=True, null=True)
    specialization = models.ForeignKey(
        acmodels.Specialization,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        """Meta definition for Student."""

        ordering = ['id']
        verbose_name = _("Student")
        verbose_name_plural = _("Students")

    def save(self, *args, **kwargs):
        if self.user.specialization and self.specialization != self.user.specialization:
            self.specialization = self.user.specialization
        super(Student, self).save(*args, **kwargs)  # Call the real save() method

    def __str__(self):
        """String representation of Student."""
        # return f"{self.matric_no if self.matric_no else self.student_id}"
        return f"{self.matric_no or self.student_id or self.user.email} - {self.user.first_name} {self.user.last_name} - {self.user.email}"

    def get_current_course_registrations(self, session, semester):
        return CourseRegistration.objects.filter(student=self, session__is_current=True, semester=semester)

    def get_all_course_registrations(self):
        return CourseRegistration.objects.filter(student=self)

    def department(self):
        try:
            dept = self.specialization.department
            return dept.name
        except Exception:
            return None

    def faculty(self):
        try:
            dept = self.specialization.department
            faculty = dept.faculty
            return faculty.name
        except Exception:
            return None

    def level(self):
        try:
            lvl = self.academic_data.first().level
            return lvl.code
        except Exception:
            return None
        
    def notices(self):
        try:
            notices = utils.get_all_user_notices(self.user)
            return notices
        except:
            return None
        
    def information(self):
        try:
            information = utils.get_all_user_information(self.user)
            return information
        except:
            return None


class CourseAdviser(models.Model):
    """Model definition for CourseAdviser"""

    staff = models.ForeignKey(Staff, limit_choices_to={'is_active': True}, on_delete=models.CASCADE)
    specialization = models.ForeignKey(
        acmodels.Specialization,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True
    )
    department = models.ForeignKey(
        acmodels.Department,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    level = models.ForeignKey(acmodels.Level, on_delete=models.CASCADE, null=True)
    session = models.ForeignKey(acmodels.Session, on_delete=models.CASCADE, null=True)
    semester = models.ForeignKey(acmodels.Semester, on_delete=models.CASCADE, null=True)

    class META:
        """Meta definition for CourseAdviser."""

        ordering = ['id']
        verbose_name = _("CourseAdviser")
        verbose_name_plural = _("CourseAdvisers")

    def save(self, *args, **kwargs):
        self.staff.is_course_adviser = True
        self.staff.save()
        super(CourseAdviser, self).save(*args, **kwargs)  # Call the real save() method

    def __str__(self):
        """String representation of CourseAdviser."""
        return f"{self.staff}"


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
    birthday = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    nationality = models.CharField(max_length=250, null=True, blank=True)
    state_of_origin = models.CharField(max_length=250, null=True, blank=True)
    local_govt = models.CharField(max_length=250, null=True, blank=True)
    permanent_address = models.CharField(max_length=250, null=True, blank=True)
    address = models.CharField(max_length=250, null=True, blank=True)
    phone_no_1 = models.CharField(max_length=20, null=True, blank=True)
    phone_no_2 = models.CharField(max_length=20, null=True, blank=True)
    profile_picture = models.ImageField(blank=True, null=True, upload_to='images/profile_pictures/')

    class Meta:
        """Meta definition for Biodata."""

        ordering = ['id']
        verbose_name = _("Biodata")
        verbose_name_plural = _("Biodata")

    def __str__(self):
        """String representation of Biodata."""
        if self.user.first_name and self.user.last_name:
            return f"{self.user.last_name} {self.user.first_name}"
        else:
            return f"{self.user.email}"


class AcademicData(models.Model):
    """Model definition for AcademicData."""

    # Definitions for model choices
    class QualificationChoices(models.TextChoices):
        BSC = 'B.Sc', _('B.Sc')
        MSC = 'M.Sc', _('M.Sc')
        OTHER = 'Other', _('Other')

    student = models.OneToOneField(
        Student,
        on_delete=models.CASCADE,
        related_name='academic_data'
    )
    specialization = models.ForeignKey(
        acmodels.Specialization,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    department = models.ForeignKey(acmodels.Department, on_delete=models.CASCADE, null=True)
    level = models.ForeignKey(acmodels.Level, on_delete=models.CASCADE, null=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True, blank=True)
    qualification = models.CharField(
        max_length=250,
        choices=QualificationChoices.choices,
        null=True,
        default=QualificationChoices.OTHER,
    )
    session = models.ForeignKey(acmodels.Session, on_delete=models.CASCADE, null=True)
    semester = models.ForeignKey(acmodels.Semester, on_delete=models.CASCADE, null=True)

    class Meta:
        """Meta definition for AcademicData."""

        ordering = ['id']
        verbose_name = _("AcademicData")
        verbose_name_plural = _("AcademicData")

    def __str__(self):
        """String representation of AcademicData."""
        return f"{self.student.matric_no if self.student.matric_no else self.student.student_id}"

    def get_gpa(self):
        return None

    def get_cgpa(self):
        return None
    
    def course_adviser(self):
        try:
            course_adviser = CourseAdviser.objects.get(
                specialization=self.specialization,
                level=self.level
            )
            return course_adviser
        except:
            return None


class CourseRegistration(models.Model):
    """Model definition for CourseRegistration."""

    course = models.ForeignKey(acmodels.Course, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    session = models.ForeignKey(acmodels.Session, on_delete=models.CASCADE, null=True)
    semester = models.ForeignKey(acmodels.Semester, on_delete=models.CASCADE, null=True)
    is_active = models.BooleanField(default=True)
    is_completed = models.BooleanField(default=False)
    is_passed = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta:
        """Meta definition for CourseRegistration."""

        ordering = ['id']
        verbose_name = _('CourseRegistration')
        verbose_name_plural = _('CourseRegistrations')

    def __str__(self):
        """String representation of CourseRegistration."""
        return f"{self.course.name} - registration"


class Result(models.Model):
    """Model definition for Result."""

    score = models.FloatField()
    course = models.ForeignKey(acmodels.Course, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    session = models.ForeignKey(acmodels.Session, on_delete=models.CASCADE, null=True)
    semester = models.ForeignKey(acmodels.Semester, on_delete=models.CASCADE, null=True)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.BooleanField(default=False)
    update_reason = models.TextField(null=True, blank=True)
    update_timestamp = models.DateTimeField(auto_now=True, auto_now_add=False)

    class Meta:
        """Meta definition for Result."""

        ordering = ['id']
        verbose_name = _('Result')
        verbose_name_plural = _('Results')

    def __str__(self):
        """String representation of Result."""
        return f"{self.score} of 100"
    
    def get_value(self):
        try:
            if self.score / 100.00 >= 0.5:
                return 'Pass'
            elif self.score == 0:
                return "Not Available"
            else:
                return 'Fail'
        except Exception:
            return None
        
    def get_grade(self):
        try:
            if self.score / 100.00 >= 0.9:
                return 'A+'
            elif self.score / 100.00 >= 0.8:
                return 'A'
            elif self.score / 100.00 >= 0.7:
                return 'B'
            elif self.score / 100.00 >= 0.6:
                return 'C'
            elif self.score / 100.00 >= 0.5:
                return 'D'
            elif self.score / 100.00 >= 0.4:
                return 'E'
            elif self.score == 0:
                return "Not Available"
            else:
                return 'F'
        except Exception:
            return None


class AcademicHistory(models.Model):
    """Model definition for AcademicHistory."""

    # Definitions for model choices
    class QualificationChoices(models.TextChoices):
        JSSCE = 'JSSCE', _('JSSCE')
        SSCE = 'SSCE', _('SSCE')
        BACHELORS = 'Bachelors', _('Bachelors')
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

        ordering = ['id']
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
    STIs = models.TextField(null=True, blank=True)
    heart_disease = models.TextField(null=True, blank=True)
    disabilities = models.TextField(null=True, blank=True)
    respiratory_problems = models.TextField(null=True, blank=True)

    class Meta:
        """Meta definition for HealthData."""

        ordering = ['id']
        verbose_name = _("HealthData")
        verbose_name_plural = _("HealthData")

    def __str__(self):
        """String representation of HealthData."""
        return f"{self.biodata}"


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

        ordering = ['id']
        verbose_name = _("FamilyData")
        verbose_name_plural = _("FamilyData")

    def __str__(self):
        """String representation of FamilyData."""
        return f"{self.biodata}"
