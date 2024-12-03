from django.contrib import admin

from announce.models import (
    Announce,
    AnnounceFile,
    AnnounceImage,
    Comment,
)

# Register your models here.

# admin.site.register(Announce)


@admin.register(Announce)
class AnnounceAdmin(admin.ModelAdmin):
    """
    ModelAdmin for Announce

    Attributes:
        list_display:
        list_filter:
        search_fields:
    """

    list_display = (
        "is_type",
        "status",
        "author",
        "title",
        "created_at",
        "updated_at",
        "is_delete",
    )
    list_filter = (
        "is_type",
        "status",
        "author",
        "title",
        "detail",
        "created_at",
        "updated_at",
        "is_delete",
    )
    search_fields = (
        "is_type",
        "status",
        "author",
        "title",
        "detail",
        "created_at",
        "updated_at",
        "is_delete",
    )


@admin.register(AnnounceImage)
class AnnounceImageAdmin(admin.ModelAdmin):
    """
    ModelAdmin for AnnounceImage

    Attributes:
        list_display:
        list_filter:
        search_fields:
    """

    list_display = (
        "announce",
        "images",
    )
    list_filter = (
        "announce",
        "images",
    )
    search_fields = (
        "announce",
        "images",
    )


admin.site.register(AnnounceFile)
# admin.site.register(AnnounceImage)
admin.site.register(Comment)
