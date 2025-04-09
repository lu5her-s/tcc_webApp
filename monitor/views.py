from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import DetailView, ListView

from account.models import Sector

from .models import Monitor

# Create your views here.


class MonitorHomeView(LoginRequiredMixin, ListView):
    model = Monitor
    template_name = "monitor/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["sectors"] = Sector.objects.all()
        return context


class MonitorDetailView(LoginRequiredMixin, DetailView):
    model = Monitor

    def get(self, request, pk):
        return render(request, "monitor/detail.html")
