from django.contrib import admin
from .models import (
    ParcelRequest,
    RequestItem,
    RequestBillDetail,
    ParcelRequestNote,
    RejectBillNote,
    ParcelReturn,
    ParcelReturnItem,
    ParcelReturnDetail,
    ParcelReturnBillNote,
    RejectReturnBillNote,
)

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

@admin.register(ParcelRequestNote)
class ParcelRequestNoteAdmin(admin.ModelAdmin):
    list_filter = ('bill',)
    search_fields = ('bill',)
    list_display = ('bill', 'note')
    raw_id_fields = ('bill', 'user')

@admin.register(RejectBillNote)
class RejectBillNoteAdmin(admin.ModelAdmin):
    list_filter = ('bill',)
    search_fields = ('bill',)
    list_display = ('bill', 'note')
    raw_id_fields = ('bill', 'user')

@admin.register(ParcelReturn)
class ParcelReturnAdmin(admin.ModelAdmin):
    search_fields = ('pk', 'user', 'created_at',)

    def bill_no(self, obj):
        return f'{obj.pk}/{obj.created_at.year+543}'

    def stock(self, obj):
        return obj.stock_reciever.name

    # list_filter = ('user', 'created_at', 'stock')
    list_display = ('bill_no', 'user', 'created_at', 'stock', 'status')

@admin.register(ParcelReturnItem)
class ParcelReturnItemAdmin(admin.ModelAdmin):
    list_filter = ('bill', 'item',)
    search_fields = ('bill', 'item',)

    def bill_no(self, obj):
        return f'{obj.bill.pk}/{obj.bill.created_at.year+543}'

    list_display = ('bill_no', 'item')

@admin.register(ParcelReturnDetail)
class ParcelReturnDetailAdmin(admin.ModelAdmin):
    # add stock to list filter
    list_filter = ('bill', )
    search_fields = ('bill',)

    def bill_no(self, obj):
        return f'{obj.bill.pk}/{obj.bill.created_at.year+543}'

    def stock(self, obj):
        return obj.bill.stock

    list_display = ('bill_no', 'stock')

@admin.register(ParcelReturnBillNote)
class ParcelReturnBillNoteAdmin(admin.ModelAdmin):
    list_filter = ('bill',)
    search_fields = ('bill',)
    list_display = ('bill', 'note')
    raw_id_fields = ('bill', 'user')

@admin.register(RejectReturnBillNote)
class RejectReturnBillNoteAdmin(admin.ModelAdmin):
    list_filter = ('bill',)
    search_fields = ('bill',)
    list_display = ('bill', 'note')
    raw_id_fields = ('bill', 'user')
