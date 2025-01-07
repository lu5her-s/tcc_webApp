from .models import CarBooking
from django.db.models import Q


def car_booking(request):
    try:
        if request.user.groups.filter(name="Command").exists():
            return {"car_booking": CarBooking.objects.all()}
        else:
            return {
                "car_booking": CarBooking.objects.filter(approver=request.user.profile)
            }
    except:
        return {"car_booking": None}
