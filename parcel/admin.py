from django.contrib import admin
from .models import RequestBill

# Register your models here.

# admin.site.register(RequestBill)
@admin.register(RequestBill)
class RequestBillAdmin(admin.ModelAdmin):
    list_filter = ('user', 'created_at', 'receiver')
    search_fields = ('pk', 'user', 'created_at', 'receiver')

    def bill_no(self, obj):
        return f'{obj.pk}/{obj.created_at.year+543}'

    def department(self, obj):
        if obj.receiver:
            return obj.receiver.department
        else:
            return obj.user.profile.department if obj.user.profile.department else None

    list_display = ('bill_no', 'user', 'created_at', 'receiver')
