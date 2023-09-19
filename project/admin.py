from django.contrib import admin
from .models import Project, Issue, Comment, Contributor


class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "author", "created_time")


admin.site.register(Project, ProjectAdmin)


class IssueAdmin(admin.ModelAdmin):
    list_display = ("name", "author", "created_time")


admin.site.register(Issue, IssueAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ("author", "issue", "created_time")


admin.site.register(Comment, CommentAdmin)


class ContributorAdmin(admin.ModelAdmin):
    list_display = ("user", "project")


admin.site.register(Contributor, ContributorAdmin)