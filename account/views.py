#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : views.py
# Author            : lu5her <lu5her@mail>
# Date              : Thu Sep, 29 2022, 11:58 272
# Last Modified Date: Thu Sep, 29 2022, 13:36 272
# Last Modified By  : lu5her <lu5her@mail>
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
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
    template_name = 'account/register1.html'
    success_url = reverse_lazy('login')
