from django.contrib import admin

from car.models import (
    Car,
    CarAfterFixImage,
    CarBooking,
    CarFix,
    CarFixImage,
    CarImage,
    Refuel,
)

# Register your models here.

# admin.site.register(Car)
admin.site.register(CarBooking)
admin.site.register(CarFix)
admin.site.register(Refuel)
admin.site.register(CarImage)
admin.site.register(CarFixImage)
# register CarAfterFixImage
admin.site.register(CarAfterFixImage)
# register CarFixStatus


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    """CarAdmin. general car detail"""

    list_display = (
        "number",
        "fuel_now",
        "responsible_man",
        "mile_now",
        "status",
    )
    list_filter = (
        "responsible_man",
        "status",
    )
    search_fields = (
        "status",
        "number",
    )
