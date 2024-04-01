from .models import Announce

def announce_not_read(request):
    try:
        return {'announce_not_read': Announce.objects.filter(
            ~Q(author=request.user) & ~Q(
                reads__id=request.user.id)
        )}
    except:
        return {'announce_not_read': None}
