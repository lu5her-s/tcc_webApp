from django.db.models import Q
from assign.models import Assign
from announce.models import Announce
from document.models import Department, Document


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


def document_not_accepted(request):
    all_inbox = Document.objects.filter(
        assigned_sector=request.user.profile.sector).count()
    all_department = Department.objects.filter(
        reciever__profile__sector=request.user.profile.sector).count()
    # context['new_inbox'] = str(abs(all_inbox - all_department))
    return {'document_not_accepted': str(abs(all_inbox - all_department))}


def count_total(request):
    total_notification = 0
    assign_not_accepted_count = len(
        assign_not_accepted(request)['assign_not_accepted'])
    announce_not_read_count = len(
        announce_not_read(request)['announce_not_read']
    )
    document_not_accepted_count = len(
        document_not_accepted(request)['document_not_accepted']
    )
    total_notification = assign_not_accepted_count + announce_not_read_count + document_not_accepted_count
    return {'count_total': total_notification}
