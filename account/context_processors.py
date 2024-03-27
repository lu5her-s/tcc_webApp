from django.db.models import Q
from assign.models import Assign
from announce.models import Announce
from document.models import Department, Document
from inform.models import Inform
from asset.models import ItemOnHand


def assign_not_accepted(request):
    try:
        return {'assign_not_accepted': Assign.objects.filter(
            assigned_to=request.user.profile,
            accepted=False
        )}
    except:
        return {'assign_not_accepted': None}


def announce_not_read(request):
    try:
        return {'announce_not_read': Announce.objects.filter(
            ~Q(author=request.user) & ~Q(
                reads__id=request.user.id)
        )}
    except:
        return {'announce_not_read': None}


def document_not_accepted(request):
    try:
        all_inbox = Document.objects.filter(
            assigned_sector=request.user.profile.sector)
        all_department = Department.objects.filter(
            reciever__profile__sector=request.user.profile.sector)
        not_accepted = abs(len(all_inbox) - len(all_department))
        # context['new_inbox'] = str(abs(all_inbox - all_department))
        return {'document_not_accepted': not_accepted}
    except:
        return {'document_not_accepted': None}

def new_inform(request):
    try:
        if request.user.groups.filter(name__in=['Manager', 'Technical', 'Command']).exists():
            new_inform = Inform.objects.filter(
                inform_status=Inform.InformStatus.INFORM
                )
            return {'new_inform': new_inform}
        else:
            return {'new_inform': None}
    except:
        return {'new_inform': None}

def count_total(request):
    try:
        total_notification = 0
        assign_not_accepted_count = Assign.objects.filter(
            assigned_to=request.user.profile,
            accepted=False
        ).count()

        announce_not_read_count = Announce.objects.filter(
            ~Q(author=request.user) & ~Q(reads__id=request.user.id)
        ).count()

        all_inbox = Document.objects.filter(
            assigned_sector=request.user.profile.sector)
        all_department = Department.objects.filter(
            reciever__profile__sector=request.user.profile.sector)
        document_not_accepted_count = abs(len(all_inbox) - len(all_department))
        new_inform_count = 0
        if request.user.groups.filter(name__in=['Manager', 'Technical', 'Command']).exists():
            new_inform_count = Inform.objects.filter(
                inform_status=Inform.InformStatus.INFORM
                ).count()

        total_notification = assign_not_accepted_count + announce_not_read_count + document_not_accepted_count \
        + new_inform_count
        return {'count_total': total_notification}
    except:
        return {'count_total': None}

def items_on_hand(request):
    try:
        return {'items_on_hand': ItemOnHand.objects.filter(
            user=request.user
        )}
    except:
        return {'items_on_hand': None}
