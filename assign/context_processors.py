from .models import Assign


def assign_not_accepted(request):
    return {'assign_not_accepted': Assign.objects.filter(
        assigned_to=request.user.profile,
        accepted=False
    )}
