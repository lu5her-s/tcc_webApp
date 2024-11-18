from django.contrib import admin
from asset.models import (
    Category,
    ItemOnHand,
    Manufacturer,
    Supplier,
    Network,
    StockItem,
    StockItemImage,
    ItemHistory,
)

# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "created_at", "updated_at")
    list_filter = ("created_at", "updated_at")
    search_fields = ("name",)


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "contact_no",
        "address",
    )
    list_filter = ("created_at", "updated_at")
    search_fields = ("name",)


@admin.register(Network)
class NetworkAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "ip_addr",
    )
    list_filter = ("created_at", "updated_at")
    search_fields = (
        "name",
        "ip_addr",
    )


@admin.register(StockItem)
class StockItemAdmin(admin.ModelAdmin):
    list_display = (
        "item_name",
        "category",
        "serial",
        "supplier",
        "network",
        "stock_control",
        "status",
    )
    list_filter = ("category", "supplier", "network", "created_at", "updated_at")
    search_fields = (
        "item_name",
        "serial",
        "location",
    )


@admin.register(ItemOnHand)
class ItemOnHandAdmin(admin.ModelAdmin):
    def user_profile(self) -> str:
        return self.user.get_full_name()

    list_display = ("item", user_profile, "created_at")
    list_filter = (
        "item",
        "user__profile",
        "created_at",
    )
    search_fields = ("item", "user")


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "created_at", "updated_at")
    list_filter = ("created_at", "updated_at")
    search_fields = ("name",)


@admin.register(ItemHistory)
class ItemHistoryAdmin(admin.ModelAdmin):
    def user_profile(self) -> str:
        return self.user.get_full_name()

    list_display = ("item", user_profile, "description", "created_at")
    list_filter = (
        "item__item_name",
        "user__profile",
        "created_at",
    )
    search_fields = ("item", "user__profile")


admin.site.register(StockItemImage)
# admin.site.register(Manufacturer)
