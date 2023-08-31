from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

# Create your views here.


class HomeView(LoginRequiredMixin, TemplateView):
    def get_template_names(self):
        user = self.request.user
        template_name = {
            'admin': 'stock/home_admin.html',
            'default': 'stock/home.html',
        }.get(user.groups.first().name, 'default')
        return [template_name]

