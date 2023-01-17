from django.shortcuts import (
    render,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    TemplateView,
    ListView,
)

from .models import Inform

# Create your views here.


class RepairHome(LoginRequiredMixin, TemplateView):
    """
    RepairHome.
    Show Home page of Repair app
    context = [
        inform status = INF
    ]
    """

    template_name = 'repair/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['inform'] = Inform.objects.filter(
            status=Inform.RepairStatus.INF)
        return context


class InformListView(LoginRequiredMixin, ListView):
    """
    InformListView.
    show only inform status == inform
    """

    template_name = 'repair/inform.html'
    model = Inform

    def get_queryset(self):
        return super().get_queryset().filter(status = Inform.RepairStatus.INF)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'รายการแจ้งซ่อม'
        return context
