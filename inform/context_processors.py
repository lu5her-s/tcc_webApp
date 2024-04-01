from .models import Inform

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
