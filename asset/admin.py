from django.contrib import admin
from asset.models import (
    Category,
    Manufacturer,
    Supplier,
    Network,
    StockItem,
    StockItemImage,
)

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('name',)

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_no', 'address',)
    list_filter = ('created_at', 'updated_at')
    search_fields = ('name',)

@admin.register(Network)
class NetworkAdmin(admin.ModelAdmin):
    list_display = ('name', 'ip_addr',)
    list_filter = ('created_at', 'updated_at')
    search_fields = ('name', 'ip_addr',)

@admin.register(StockItem)
class StockItemAdmin(admin.ModelAdmin):
    list_display = ('item_name', 'category', 'serial', 'supplier', 'network', 'location')
    list_filter = ('category', 'supplier', 'network', 'created_at', 'updated_at')
    search_fields = ('item_name', 'serial', 'location',)

admin.site.register(StockItemImage)
admin.site.register(Manufacturer)
