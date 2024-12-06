from django.contrib import admin

from journal.models import Journal, JournalImage

# Register your models here.

# admin.site.register(Journal)
admin.site.register(JournalImage)


@admin.register(Journal)
class JournalAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "category",
        "author",
        "status",
        "created_at",
    )
    list_filter = ("category", "title", "author", "status")
