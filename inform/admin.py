from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from .models import Inform

# Register your models here.


@admin.register(Inform)
class InformAdmin(admin.ModelAdmin):
    # list_display = ('urgency', 'issue_safe', 'issue_category', 'full_name', 'created_at')
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

    def colored_urgency(self, obj):
        """colored_urgency.
        return colored urgency based on value

        :param obj:
        """
        if obj.urgency == 'HIG':
            return format_html('<span style="color: #FF0000;">{}</span>', obj.get_urgency_display())
        else:
            return obj.urgency
    colored_urgency.short_description = 'Urgency'

    list_display = ('colored_urgency', 'issue_safe', 'issue_category',
                    'full_name', 'created_at')

