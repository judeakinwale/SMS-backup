from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

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


class Programme(models.Model):
    """Model definition for Programme."""

    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    name = models.CharField(max_length=250, unique=True)
    code = models.CharField(max_length=250, null=True, blank=True, unique=True)
    max_level = models.ForeignKey("Level", on_delete=models.DO_NOTHING, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta:
        """Meta definition for Programme."""

        verbose_name = _('Programme')
        verbose_name_plural = _('Programmes')

    def __str__(self):
        """String representation of Programme."""
        return self.name


class Course(models.Model):
    """Model definition for Course."""

    programme = models.ForeignKey(Programme, on_delete=models.CASCADE)
    name = models.CharField(max_length=250, unique=True)
    code = models.CharField(max_length=250, null=True, blank=True, unique=True)
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
        null=True,
        default=LevelChoices.ONE,
    )

    class Meta:
        """Meta definition for Level."""

        verbose_name = _('Level')
        verbose_name_plural = _('Levels')

    def __str__(self):
        """String representation of Level"""
        return f"{self.code}"
