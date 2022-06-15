from django.contrib import admin
from information import models

# Register your models here.

class InformationAdmin(admin.ModelAdmin):
  list_display = ["source", "scope", "title", "body", "timestamp",]
  list_display_links = ["timestamp",]
  list_filter = ["source", "scope", "title", "body", "timestamp",]
  list_editable = ["source", "scope", "title",]
  

class NoticeAdmin(InformationAdmin):
  list_display = ["source", "scope", "title", "message", "timestamp",]
  list_filter = ["source", "scope", "title", "message", "timestamp",]
  
  
class ScopeAdmin(admin.ModelAdmin):
  list_display = ["faculty", "department", "specialization", "course", "level", "description", "is_general", "is_first_year", "is_final_year", "timestamp",]
  list_display_links = ["timestamp",]
  list_filter = ["faculty", "department", "specialization", "course", "level", "description", "is_general", "is_first_year", "is_final_year", "timestamp",]
  list_editable = ["level", "is_general", "is_first_year", "is_final_year",]
  

class InformationImageAdmin(admin.ModelAdmin):
  list_display = ["information", "image", "description", "timestamp",]
  list_display_links = ["timestamp",]
  list_filter = ["information", "image", "description", "timestamp",]
  list_editable = ["information", "image", "description",]


admin.site.register(models.Information, InformationAdmin)
admin.site.register(models.InformationImage, InformationImageAdmin)
admin.site.register(models.Notice, NoticeAdmin)
admin.site.register(models.Scope, ScopeAdmin)
