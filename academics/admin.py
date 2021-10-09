from django.contrib import admin
from academics import models

# Register your models here.

admin.site.register(models.Faculty)
admin.site.register(models.Department)
admin.site.register(models.Specialization)
admin.site.register(models.Course)
admin.site.register(models.Level)
admin.site.register(models.Semester)
admin.site.register(models.Session)
admin.site.register(models.RecommendedCourses)
