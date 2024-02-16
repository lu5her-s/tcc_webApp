from django.contrib import admin
from .models import ParcelRequest, RequestItem, RequestBillDetail

# Register your models here.

# admin.site.register(RequestBill)
@admin.register(ParcelRequest)
class RequestBillAdmin(admin.ModelAdmin):
    list_filter = ('user', 'created_at', 'stock')
    search_fields = ('pk', 'user', 'created_at',)

    def bill_no(self, obj):
        return f'{obj.pk}/{obj.created_at.year+543}'

    def department(self, obj):
        if obj.receiver:
            return obj.receiver.department
        else:
            return obj.user.profile.department if obj.user.profile.department else None

    list_display = ('bill_no', 'user', 'created_at', 'stock')


# admin.site.register(RequestItem)
@admin.register(RequestItem)
class RequestItemAdmin(admin.ModelAdmin):
    list_filter = ('bill', 'item',)
    search_fields = ('bill', 'item',)

    def bill_no(self, obj):
        return f'{obj.bill.pk}/{obj.bill.created_at.year+543}'

    list_display = ('bill_no', 'item', 'quantity', 'total_price')

# admin.site.register(RequestBillDetail)
@admin.register(RequestBillDetail)
class RequestBillDetailAdmin(admin.ModelAdmin):
    # add stock to list filter
    list_filter = ('bill', 'bill__stock')
    search_fields = ('bill',)

    def bill_no(self, obj):
        return f'{obj.bill.pk}/{obj.bill.created_at.year+543}'

    def stock(self, obj):
        return obj.bill.stock

    list_display = ('bill_no', 'stock')
