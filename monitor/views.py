from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import View

from .models import Monitor

# Create your views here.


class MonitorHomeView(LoginRequiredMixin, View):
    model = Monitor

    def get(self, request):
        return render(request, "monitor/home.html")


class MonitorDetailView(LoginRequiredMixin, View):
    model = Monitor

    def get(self, request, pk):
        return render(request, "monitor/detail.html")
