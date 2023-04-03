from .models import Inform


def new_inform(request):
    new_inform = Inform.objects.filter(
        inform_status=Inform.InformStatus.INFORM
    )
    return {'new_inform': new_inform}
