from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from academics import models as amodels

# Create your models here.


class Information(models.Model):
    """Model definition for Information."""

    source = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        # limit_choices_to={'is_staff': True}
    )
    scope = models.ForeignKey("Scope", on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta:
        """Meta definition for Information."""

        ordering = ['id']
        verbose_name = _("Information")
        verbose_name_plural = _("Information")

    def __str__(self):
        """String representation of Information."""
        return f"{self.title} for {self.scope}"


class Notice(models.Model):
    """Model definition for Notice."""

    source = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    scope = models.ForeignKey("Scope", on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta:
        """Meta definition for Notice."""

        ordering = ['id']
        verbose_name = _("Notice")
        verbose_name_plural = _("Notices")

    def __str__(self):
        """String representation of Notice."""
        return self.title


class Scope(models.Model):
    """Model definition for Scope."""

    faculty = models.ForeignKey(amodels.Faculty, on_delete=models.CASCADE, null=True, blank=True)
    department = models.ForeignKey(amodels.Department, on_delete=models.CASCADE, null=True, blank=True)
    specialization = models.ForeignKey(
        amodels.Specialization,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    course = models.ForeignKey(amodels.Course, on_delete=models.CASCADE, null=True, blank=True)
    level = models.ForeignKey(amodels.Level, on_delete=models.CASCADE, null=True, blank=True)

    description = models.CharField(max_length=250, null=True, blank=True)
    is_general = models.BooleanField(default=True)
    is_first_year = models.BooleanField(default=False)
    is_final_year = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta:
        """Meta definition for Scope."""

        ordering = ['id']
        verbose_name = _("Scope")
        verbose_name_plural = _("Scopes")

    def __str__(self):
        """String representation of Scope."""
        return self.description


class InformationImage(models.Model):
    """Model definition for InformationImage."""

    information = models.ForeignKey("Information", related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to="images/%Y/%m/%d/", null=True)
    description = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta:
        """Meta definition for InformationImage."""

        ordering = ['id']
        verbose_name = _("Information Image")
        verbose_name_plural = _("Information Images")

    def __str__(self):
        """String representation of InformationImage."""
        return self.description
