from django.contrib import admin

from .models import Diary, Note


@admin.register(Diary)
class DiaryAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "expiration", "kind", "user")
    list_filter = ("kind", "user", "title")
    search_fields = ("title",)
    ordering = ("id",)


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ("id", "text", "diary")
    list_filter = (
        "id",
        "diary",
    )
    search_fields = ("id",)
    ordering = ("id",)
