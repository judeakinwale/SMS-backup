from django.contrib import admin
from user import models

# Register your models here.


admin.site.register(models.User)
admin.site.register(models.Staff)
admin.site.register(models.Student)
admin.site.register(models.Biodata)
admin.site.register(models.AcademicData)
admin.site.register(models.AcademicHistory)
admin.site.register(models.HealthData)
admin.site.register(models.FamilyData)
