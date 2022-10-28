from django.contrib import admin
from assign.models import Assign, AssignImage, AssignStatus, AssignProgress

# Register your models here.


@admin.register(Assign)
class AssingAdmin(admin.ModelAdmin):
    list_display = ['title', 'body', 'author', 'created_at', 'assigned_to', 'accepted',]
    list_filter  = ['title', 'body', 'author', 'created_at', 'assigned_to', 'accepted',]


admin.site.register(AssignImage)
admin.site.register(AssignStatus)
admin.site.register(AssignProgress)
