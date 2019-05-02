from django.contrib import admin
from .models import Project, IRBRecord, ProjectCategory, ProjectSubCategory, Publication

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

@admin.register(IRBRecord)
class IRBRecordAdmin(admin.ModelAdmin):
    list_display = ('irbcode', 'submitdate', 'creator', 'project', 'status')
    list_filter = ('status', 'submitdate', 'creator')
    date_hierarchy = 'submitdate'
    ordering = ('status', 'submitdate')


@admin.register(ProjectCategory)
class ProjectCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ('name',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(ProjectSubCategory)
class ProjectSubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ('name',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = ('pubdate', 'title', 'creator', 'added_at', 'updated_at')
    ordering = ('pubdate',)
    search_fields = ('title',)