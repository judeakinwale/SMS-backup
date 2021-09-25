from django.contrib import admin
from .models import User, BioData, FamilyData, HealthData, AcademicData
# Register your models here.
admin.site.register(User)
admin.site.register(BioData)
admin.site.register(FamilyData)
admin.site.register(HealthData)
admin.site.register(AcademicData)