from django.contrib import admin

from announce.models import (
    AnnounceType, 
    AnnounceStatus, 
    Announce,
    AnnounceImage,
    AnnounceFile,
    Comment,
)

# Register your models here.

# admin.site.register(Announce)
@admin.register(Announce)
class AnnounceAdmin(admin.ModelAdmin):
    list_display = ('is_type', 'status', 'author', 'title', 'created_at', 'updated_at', 'is_delete',)
    list_filter = ('is_type', 'status', 'author', 'title', 'detail', 'created_at', 'updated_at', 'is_delete',)
    search_fields = ('is_type', 'status', 'author', 'title', 'detail', 'created_at', 'updated_at', 'is_delete',)

admin.site.register(AnnounceType)
admin.site.register(AnnounceStatus)
admin.site.register(AnnounceFile)
admin.site.register(AnnounceImage)
admin.site.register(Comment)
