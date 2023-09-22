from django.contrib import admin
from .models import (
    RelayStockBill,
    DataStockBill,
    SatteliteStockBill,
    AirStockBill
)

# Register your models here.

@admin.register(RelayStockBill)
class RelayStockBillAdmin(admin.ModelAdmin):
    def id_bill(self, obj):
        created_at = obj.created_at.year + 543
        bill = f'{obj.pk}/{created_at}'
        return bill

    list_display = ('id_bill', 'item', 'qty', 'created_at', 'inform_request')
    list_filter = ('item', 'created_at', 'inform_request')
    search_fields = ('id_bill', 'item', 'created_at', 'inform_request')


@admin.register(DataStockBill)
class DataStockBillAdmin(admin.ModelAdmin):
    def id_bill(self, obj):
        created_at = obj.created_at.year + 543
        bill = f'{obj.pk}/{created_at}'
        return bill

    list_display = ('id_bill', 'item', 'qty', 'created_at', 'inform_request')
    list_filter = ('item', 'created_at', 'inform_request')
    search_fields = ('id_bill', 'item', 'created_at', 'inform_request')


@admin.register(SatteliteStockBill)
class SatteliteStockBillAdmin(admin.ModelAdmin):
    def id_bill(self, obj):
        created_at = obj.created_at.year + 543
        bill = f'{obj.pk}/{created_at}'
        return bill

    list_display = ('id_bill', 'item', 'qty', 'created_at', 'inform_request')
    list_filter = ('item', 'created_at', 'inform_request')
    search_fields = ('id_bill', 'item', 'created_at', 'inform_request')


@admin.register(AirStockBill)
class AirStockBillAdmin(admin.ModelAdmin):
    def id_bill(self, obj):
        created_at = obj.created_at.year + 543
        bill = f'{obj.pk}/{created_at}'
        return bill

    list_display = ('id_bill', 'item', 'qty', 'created_at', 'inform_request')
    list_filter = ('item', 'created_at', 'inform_request')
    search_fields = ('id_bill', 'item', 'created_at', 'inform_request')
