from django.contrib import admin

from .models import (
    Inform,
    Repair,
)

# Register your models here.

# admin.site.register(Inform)
admin.site.register(Repair)


@admin.register(Inform)
class InformAdmin(admin.ModelAdmin):
    list_display = ('pk', 'issue', 'issue_category', 'full_name', 'created_at')
    # change pk to no.
    list_display_links = ('pk', 'issue')
    list_filter = ('created_at',)
    search_fields = ('issue',)

    def full_name(self, obj):
        """full_name.
        return full name of user

        :param obj:
        """
        return obj.customer.profile
