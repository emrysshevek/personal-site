from django.contrib import admin

from home.models import Project, ProjectSample


class SampleInline(admin.TabularInline):
  model = ProjectSample
  extra = 1


class ProjectAdmin(admin.ModelAdmin):
  inlines = [SampleInline]


admin.site.register(Project, ProjectAdmin)
