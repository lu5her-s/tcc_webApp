from django.shortcuts import get_object_or_404, redirect, reverse

from .models import Inform, Repair


def repair_create(request, inform_pk):
    if request.method == "POST":
        form = request.POST
        inform = get_object_or_404(Inform, pk=inform_pk)
        repair = Repair.objects.create(
            inform=inform,
            comment=form.get("comment"),
            cost=form.get("cost"),
        )
        return redirect(reverse("repair:detail", args=[inform.pk]))
