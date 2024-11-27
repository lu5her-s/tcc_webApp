from django.contrib import admin

from assign.models import Assign, AssignImage, AssignProgress, AssignStatus

# Register your models here.


@admin.register(Assign)
class AssingAdmin(admin.ModelAdmin):
    """
    AssingAdmin for Assign app

    Attributes:
        list_display:
        list_filter:
    """

    list_display = [
        "title",
        "body",
        "author",
        "created_at",
        "assigned_to",
        "accepted",
    ]
    list_filter = [
        "title",
        "body",
        "author",
        "created_at",
        "assigned_to",
        "accepted",
    ]


admin.site.register(AssignImage)
admin.site.register(AssignStatus)
admin.site.register(AssignProgress)
