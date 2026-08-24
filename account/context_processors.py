from django.db.models import Q

from announce.models import Announce
from assign.models import Assign
from car.models import CarBooking
from document.models import Depart, Document
from inform.models import Inform
from operation.models import Operation


def assign_not_accepted(request):
    try:
        return {
            "assign_not_accepted": Assign.objects.filter(
                assigned_to=request.user.profile, accepted=False
            )
        }
    except Exception:
        return {"assign_not_accepted": None}


def announce_not_read(request):
    try:
        return {
            "announce_not_read": Announce.objects.filter(
                ~Q(author=request.user) & ~Q(reads__id=request.user.id)
            )
        }
    except Exception:
        return {"announce_not_read": None}


def _documents_not_accepted_count(user) -> int:
    """Documents assigned to the user's sector not yet accepted by anyone in it.

    Replaces the old ``abs(len(inbox) - len(accepted))`` arithmetic, which
    produced wrong counts whenever the two sets did not nest.
    """
    sector = user.profile.sector
    accepted_ids = Depart.objects.filter(
        reciever__profile__sector=sector
    ).values_list("document_id", flat=True)
    return (
        Document.objects.filter(assigned_sector=sector)
        .exclude(id__in=accepted_ids)
        .count()
    )


def document_not_accepted(request):
    try:
        return {
            "document_not_accepted": _documents_not_accepted_count(request.user)
        }
    except Exception:
        return {"document_not_accepted": None}


def new_inform(request):
    try:
        if request.user.groups.filter(
            name__in=["Manager", "Technical", "Command"]
        ).exists():
            new_inform = Inform.objects.filter(inform_status=Inform.InformStatus.INFORM)
            return {"new_inform": new_inform}
        else:
            return {"new_inform": None}
    except Exception:
        return {"new_inform": None}


def car_booking(request):
    try:
        return {
            "car_booking": CarBooking.objects.filter(
                Q(approver=request.user.profile) & Q(status=CarBooking.Status.PENDING)
            )
        }
    except Exception:
        return {"car_booking": None}


def count_total(request):
    try:
        total_notification = 0
        assign_not_accepted_count = Assign.objects.filter(
            assigned_to=request.user.profile, accepted=False
        ).count()

        announce_not_read_count = Announce.objects.filter(
            ~Q(author=request.user) & ~Q(reads__id=request.user.id)
        ).count()

        document_not_accepted_count = _documents_not_accepted_count(request.user)
        new_inform_count = 0
        if request.user.groups.filter(
            name__in=["Manager", "Technical", "Command"]
        ).exists():
            new_inform_count = Inform.objects.filter(
                inform_status=Inform.InformStatus.INFORM
            ).count()

        car_booking_count = CarBooking.objects.filter(
            Q(approver=request.user.profile) & Q(status=CarBooking.Status.PENDING)
        ).count()

        total_notification = (
            assign_not_accepted_count
            + announce_not_read_count
            + document_not_accepted_count
            + new_inform_count
            + car_booking_count
        )
        return {"count_total": total_notification}
    except Exception:
        return {"count_total": None}


# def items_on_hand(request):
#     try:
#         all_bill = ParcelRequest.objects.all()
#         items_on_hand = RequestItem.objects.filter(
#             bill__in=all_bill.filter(
#                 user=request.user
#             ),
#         ).filter(bill__billdetail__paid_status=RequestBillDetail.PaidStatus.RECEIVED)
#         return {'items_on_hand': items_on_hand}
#     except:
#         return {'items_on_hand': None}


def operation_wait_open(request):
    return {
        "operation_wait_open": list(
            Operation.objects.filter(
                author=request.user, status=Operation.ApproveStatus.WAIT_OPEN
            ).values_list("id", flat=True)
        )
    }


def operation_wait_close(request):
    return {
        "operation_wait_close": list(
            Operation.objects.filter(
                author=request.user, status=Operation.ApproveStatus.WAIT_CLOSE
            ).values_list("id", flat=True)
        )
    }
