from django.contrib import admin
from .models import Project

# Register your models here.
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('en_title', 'th_title', 'creator', 'publish', 'status')
    list_filter = ('status', 'created', 'publish', 'creator')
    search_fields = ('en_title', 'th_title', 'abstract')
    prepopulated_fields = {'slug': ('en_title',)}
    raw_id_fields = ('creator',)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')
