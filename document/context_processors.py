from .models import Department, Document

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
