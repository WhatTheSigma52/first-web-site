from django.contrib import admin

from .models import Group, Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("pk", "text", "pub_date", "author", "group")
    search_fields = ("text", "author")
    list_filter = ("pub_date",)
    list_editable = ("group",)
    empty_value_display = "~empty~"


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ("title", "description")
    search_fields = ("title",)
    empty_value_display = "~empty~"
