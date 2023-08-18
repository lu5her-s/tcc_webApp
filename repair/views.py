from django.shortcuts import (
    redirect,
    reverse,
)

from repair.models import Repair

# Create your views here.

# create repair data call from user accepted inform
def repair_create(request, inform_pk):
    if request.method == 'POST':
        form = request.POST
        repair = Repair(
            inform=Inform.objects.get(pk=inform_pk),
            comment=form['comment'],
            cost=form['cost'],
        )
        repair.save()
        return redirect(reverse('repair:detail', args=[inform_pk]))
