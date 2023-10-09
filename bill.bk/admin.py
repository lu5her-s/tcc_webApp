from django.contrib import admin
from .models import (
    RequestBill,
    RequestItem,
    RequestBillDetail
)

# Register your models here.

@admin.register(RequestBill)
class RequestBillAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'created_at', 'receiver', 'department')
    list_filter = ('user', 'created_at', 'receiver', 'department')

