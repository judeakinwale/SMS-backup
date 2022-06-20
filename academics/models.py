from django.db import models
from django.conf import settings
# from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from datetime import datetime

# Create your models here.


class Faculty(models.Model):
    """Model definition for Faculty."""

    name = models.CharField(max_length=250, unique=True)
    code = models.IntegerField(null=True, blank=True, unique=True)
    description = models.TextField(null=True, blank=True)
    dean = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        limit_choices_to={'is_staff': True},
        null=True,
        blank=True
    )
    is_active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta:
        """Meta definition for Faculty."""

        ordering = ['id']
        verbose_name = _('Faculty')
        verbose_name_plural = _('Faculty')

    def save(self, *args, **kwargs):
        if self.dean:
            try:
                dean = self.dean.staff_set.all().first()
                dean.is_dean_of_faculty = True
                dean.save()
                print(f"{dean} \n Is dean of faculty: {dean.is_dean_of_faculty}")
            except Exception:
                self.dean.get_staff()
                dean = self.dean.staff_set.all().first()
                dean.is_dean_of_faculty = True
                dean.save()
                print(f"{dean} \n Is dean of faculty: {dean.is_dean_of_faculty}")
        super(Faculty, self).save(*args, **kwargs)  # Call the real save() method

    def __str__(self):
        """String representation of Faculty."""
        return self.name


class Department(models.Model):
    """Model definition for Department."""

    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    name = models.CharField(max_length=250, unique=True)
    code = models.CharField(max_length=250, null=True, blank=True, unique=True)
    description = models.TextField(null=True, blank=True)
    head = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        limit_choices_to={'is_staff': True},
        null=True,
        blank=True
    )
    is_active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta:
        """Meta definition for Department."""

        ordering = ['id']
        verbose_name = _('Department')
        verbose_name_plural = _('Departments')

    def save(self, *args, **kwargs):
        if self.head:
            try:
                head = self.head.staff_set.all().first()
                head.is_head_of_department = True
                head.save()
                print(f"{head} \n Is head of department: {head.is_head_of_department}")
            except Exception:
                self.head.get_staff()
                head = self.head.staff_set.all().first()
                head.is_head_of_department = True
                head.save()
                print(f"{head} \n Is head of department: {head.is_head_of_department}")
        super(Department, self).save(*args, **kwargs)  # Call the real save() method

    def __str__(self):
        """String representation of Department."""
        return self.name


class Specialization(models.Model):
    """Model definition for Specialization."""

    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    name = models.CharField(max_length=250, unique=True)
    code = models.CharField(max_length=250, null=True, blank=True, unique=True)
    max_level = models.ForeignKey("Level", on_delete=models.DO_NOTHING, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta:
        """Meta definition for Specialization."""

        ordering = ['id']
        verbose_name = _('Specialization')
        verbose_name_plural = _('Specializations')

    def __str__(self):
        """String representation of Specialization."""
        return self.name


class Course(models.Model):
    """Model definition for Course."""

    specialization = models.ForeignKey(Specialization, on_delete=models.CASCADE)
    name = models.CharField(max_length=250, unique=True)
    code = models.CharField(max_length=250, null=True, blank=True, unique=True)
    unit = models.IntegerField(default=2)
    description = models.TextField(null=True, blank=True)
    coordinator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        limit_choices_to={'is_staff': True},
        null=True,
        blank=True
    )
    is_active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta:
        """Meta definition for Course."""

        ordering = ['id']
        verbose_name = _('Course')
        verbose_name_plural = _('Courses')

    def __str__(self):
        """String representation of Course."""
        return self.name


class Level(models.Model):
    """Model definition for Level."""

    class LevelChoices(models.IntegerChoices):
        ONE = 100
        TWO = 200
        THREE = 300
        FOUR = 400
        FIVE = 500

    code = models.IntegerField(
        choices=LevelChoices.choices,
        unique=True,
        null=True,
        default=LevelChoices.ONE,
    )

    class Meta:
        """Meta definition for Level."""

        ordering = ['id']
        verbose_name = _('Level')
        verbose_name_plural = _('Levels')

    def __str__(self):
        """String representation of Level"""
        return f"{self.code}"


class Semester(models.Model):
    """Model definition for Semester."""

    class SemesterChoices(models.IntegerChoices):
        FIRST = 1, '1st Semester'
        SECOND = 2, '2nd Semester'

    semester = models.IntegerField(
        choices=SemesterChoices.choices,
        unique=True,
        null=True,
        default=SemesterChoices.FIRST
    )
    is_current = models.BooleanField(default=False)

    class Meta:
        """Meta definition for Semester."""

        ordering = ['id']
        verbose_name = 'Semester'
        verbose_name_plural = 'Semesters'

    def __str__(self):
        """String representation of Semester."""
        return f"{self.semester}"


class Session(models.Model):
    """Model definition for Session."""

    year = models.CharField(max_length=4, unique=True, default=str(datetime.today().year))
    is_current = models.BooleanField(default=False)

    class Meta:
        """Meta definition for Session."""

        ordering = ['-year']
        verbose_name = 'Session'
        verbose_name_plural = 'Sessions'

    def save(self, *args, **kwargs):
        """Modify the model object's properties before saving"""
        current_year = datetime.today().year
        year = datetime.strptime(self.year, "%Y").year

        if year == current_year:
            self.is_current = True

        super(Session, self).save(*args, **kwargs)  # Call the real save() method

    def __str__(self):
        """String representation of Session."""
        return f'{self.year}/{datetime.strptime(self.year, "%Y").year + 1}'


class RecommendedCourses(models.Model):
    """Model definition for RecommendedCourses."""

    specialization = models.ForeignKey(
        Specialization,
        related_name=_("recommended_courses"),
        on_delete=models.CASCADE
    )
    source_specialization = models.ForeignKey(
        Specialization,
        related_name=_("direct_recommended_courses"),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    # courses = models.ManyToManyField(Course)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, null=True)
    level = models.ForeignKey(Level, on_delete=models.CASCADE, null=True)
    is_compulsory = models.BooleanField(default=True)

    class Meta:
        """Meta definition for RecommendedCourses."""

        ordering = ['id']
        verbose_name = _('RecommendedCourses')
        verbose_name_plural = _('RecommendedCourses')
        
    def save(self, *args, **kwargs):
        if not self.source_specialization:
            self.source_specialization = self.specialization
        super().save(*args, **kwargs)

    def __str__(self):
        """String representation of RecommendedCourses."""
        return f"Recommended courses for {self.specialization} at level: {self.level}"
