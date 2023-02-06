from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import (
    Inform,
    Repair,
)

# Register your models here.

# admin.site.register(Inform)
admin.site.register(Repair)


@admin.register(Inform)
class InformAdmin(admin.ModelAdmin):
    list_display = ('pk', 'issue_safe', 'issue_category', 'full_name', 'created_at')
    list_display_links = ('issue_safe',)
    list_filter = ('created_at',)
    search_fields = ('issue',)

    def full_name(self, obj):
        """full_name.
        return full name of user

        :param obj:
        """
        return obj.customer.profile
    full_name.short_description = 'Requester'

    def issue_safe(self, obj):
        """issue_safe.
        return safe tag for html

        :param obj:
        """
        return mark_safe(obj.issue)
    issue_safe.short_description = 'Issue'
