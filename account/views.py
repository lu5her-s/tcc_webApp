from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import (
    CreateView,
    TemplateView,
)

# Create your views here.

class HomeView(TemplateView):
    template_name = 'base.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context

class RegisterView(CreateView):

    """Docstring for RegisterView. """
    form_class = UserCreationForm
    model = User
    template_name = 'account/register.html'
