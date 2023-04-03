from django.db.models import Q
from assign.models import Assign
from announce.models import Announce


def assign_not_accepted(request):
    return {'assign_not_accepted': Assign.objects.filter(
        assigned_to=request.user.profile,
        accepted=False
    )}


def announce_not_read(request):
    return {'announce_not_read': Announce.objects.filter(
        ~Q(author=request.user) & ~Q(
            reads__id=request.user.id)
    )}


def count_total(request):
    total_notification = 0
    assign_not_accepted_count = len(
        assign_not_accepted(request)['assign_not_accepted'])
    announce_not_read_count = len(
        announce_not_read(request)['announce_not_read']
    )
    total_notification = assign_not_accepted_count + announce_not_read_count
    return {'count_total': total_notification}
