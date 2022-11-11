from django.contrib import admin
from car.models import (
    ApproveStatus,
    Car,
    CarFixImage,
    CarStatus,
    CarFix,
    CarType,
    CarBooking,
    Refuel,
    CarImage,
)

# Register your models here.

# admin.site.register(Car)
admin.site.register(CarBooking)
admin.site.register(CarStatus)
admin.site.register(CarFix)
admin.site.register(CarType)
admin.site.register(Refuel)
admin.site.register(ApproveStatus)
admin.site.register(CarImage)
admin.site.register(CarFixImage)

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    """CarAdmin. general car detail"""

    list_display = ('number', 'fuel_now', 'responsible_man', 'mile_now', 'status',)
    list_filter = ('responsible_man', 'status',)
    search_fields = ('status', 'number',)


# @admin.register(CarFix)
# class CarFixAdmin(admin.ModelAdmin):
    # """CarFixAdmin. data maintenance car"""

    # list_display = ('car.number', 'fix_requester', 'requested_at', 'fix_approve_status',)
    # list_filter = ('car.number', 'fix_requester', 'requested_at', 'fix_approve_status',)
    # search_fields = ('car.number', 'fix_requester', 'fix_approve_status')


# @admin.register(CarUse)
# class CarUseAdmin(admin.ModelAdmin):
    # """CarUseAdmin. request to use car"""

    # list_display = ('car.number', 'requester', 'driver', 'use_approve_status',)
    # list_filter = ('car.number', 'requester', 'driver', 'use_approve_status')
#     search_fields = ('car.number', 'requester', 'driver', 'use_approve_status')
