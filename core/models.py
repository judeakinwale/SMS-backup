# from django.db import models
# from django.utils.translation import gettext_lazy as _
# from user import models as umodels
# from academics import models as acmodels

# # Create your models here.



# class CourseRegistration(models.Model):
#     """Model definition for CourseRegistration."""

#     course = models.ForeignKey(acmodels.Course, on_delete=models.CASCADE)
#     student = models.ForeignKey(umodels.Student, on_delete=models.CASCADE)
#     session = models.CharField(max_length=250, null=True, blank=True)
#     semester = models.CharField(max_length=250, null=True, blank=True)
#     is_active = models.BooleanField(default=True)
#     is_completed = models.BooleanField(default=False)
#     is_passed = models.BooleanField(default=False)
#     timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

#     class Meta:
#         """Meta definition for CourseRegistration."""

#         verbose_name = _('CourseRegistration')
#         verbose_name_plural = _('CourseRegistrations')

#     def __str__(self):
#         """String representation of CourseRegistration."""
#         return f"{self.course.name} - registration"

