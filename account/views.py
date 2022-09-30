#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : views.py
# Author            : lu5her <lu5her@mail>
# Date              : Thu Sep, 29 2022, 11:58 272
# Last Modified Date: Fri Sep, 30 2022, 09:40 273
# Last Modified By  : lu5her <lu5her@mail>
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import HttpResponseRedirect, get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    TemplateView,
)

from account.models import (
    Position,
    Profile,
    Rank,
    Sector,
)
from account.forms import (
    ProfileForm,
    UserForm,
)
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash

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

class ProfileView(LoginRequiredMixin, TemplateView):
    model = User
    template_name = 'account/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_form'] = UserForm(instance=self.request.user)
        context['profile_form'] = ProfileForm(instance=self.request.user.profile)
        context['password_form'] = PasswordChangeForm(self.request.user)
        return context

def update_profile(request):
    user = get_object_or_404(User, pk=request.user.pk)
    profile = get_object_or_404(Profile, user=user)

    if request.method == 'POST':
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.email = request.POST['email']

        user.save()

        if request.FILES:
            profile.image = request.FILES.get('image')

        if request.POST['rank']:
            rank = request.POST['rank']
            profile.rank = Rank.objects.get(pk=rank)

        if request.POST['position']:
            profile.position = Position.objects.get(pk=request.POST['position'])

        if request.POST['sector']:
            profile.sector = Sector.objects.get(pk=request.POST['sector'])

        profile.place = request.POST['place']
        profile.address = request.POST['address']
        profile.phone = request.POST['phone']
        profile.twitter = request.POST['twitter']
        profile.facebook = request.POST['facebook']
        profile.instagram = request.POST['instagram']
        profile.line_id = request.POST['line_id']
        profile.line_token = request.POST['line_token']

        profile.save()
        return HttpResponseRedirect(reverse_lazy('account:profile'))

class ChangePassword(LoginRequiredMixin, PasswordChangeView):
    model = User
    form_class = PasswordChangeForm
    template_name = 'account/change_password.html'
    success_url = reverse_lazy('login')
