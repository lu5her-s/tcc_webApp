#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : views.py
# Author            : lu5her <lu5her@mail>
# Date              : Thu Sep, 29 2022, 11:58 272
# Last Modified Date: Fri Dec, 23 2022, 18:00 357
# Last Modified By  : lu5her <lu5her@mail>
import datetime
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.views import PasswordChangeView
from django.contrib.contenttypes.models import Q
from django.http import JsonResponse
from django.shortcuts import HttpResponseRedirect, get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm,   UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash

from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    TemplateView,
)

from account.models import (
    Position,
    Profile,
    Rank,
    Sector,
)
from account.models import Department as DP
from account.forms import (
    ProfileForm,
    UserForm,
)

from announce.models import (
    Announce,
    Comment,
)
from document.models import Department, Document
from inform.models import Inform
from journal.models import Journal
from assign.models import Assign


# Create your views here.

class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'base.html'

    # TODO : make context
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['announce'] = Announce.objects.all()
        context['recent_comment'] = Comment.objects.all().order_by(
            '-created_at')[:5]
        all_inbox = Document.objects.filter(
            assigned_sector=self.request.user.profile.sector).count()
        context['all_inbox'] = all_inbox
        all_department = Department.objects.filter(
            reciever__profile__sector=self.request.user.profile.sector).count()
        context['new_inbox'] = str(abs(all_inbox - all_department))
        context['journal'] = Journal.objects.filter(author=self.request.user)
        today_min = datetime.datetime.combine(
            datetime.date.today(), datetime.time.min)
        today_max = datetime.datetime.combine(
            datetime.date.today(), datetime.time.max)
        context['today_journal'] = Journal.objects.filter(
            author__profile__sector=self.request.user.profile.sector,
            created_at__range=(today_min, today_max)
        )
        try:
            context['not_read'] = Announce.objects.filter(
                ~Q(author=self.request.user) & ~Q(
                    reads__id=self.request.user.id)
            )
        except:
            pass
        if self.request.user.groups.filter(name="Staff"):
            context['assign'] = Assign.objects.filter(author=self.request.user)
            context['wait_assign'] = Assign.objects.filter(
                author=self.request.user, accepted=False)
        else:
            context['assign'] = Assign.objects.filter(
                assigned_to__user=self.request.user)
            context['wait_assign'] = Assign.objects.filter(
                assigned_to__user=self.request.user, accepted=False)

        if not self.request.user.groups.filter(name="StaffRepair"):
            context['inform_department'] = Inform.objects.filter(
                customer__profile__department=self.request.user.profile.department
            )
        context['informs'] = Inform.objects.all()

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
        context['profile_form'] = ProfileForm(
            instance=self.request.user.profile)
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
            profile.position = Position.objects.get(
                pk=request.POST['position'])

        if request.POST['sector']:
            profile.sector = Sector.objects.get(pk=request.POST['sector'])

        # profile.place      = request.POST['place']
        if request.POST['department']:
            profile.department = DP.objects.get(pk=request.POST['department'])

        profile.address = request.POST['address']
        profile.phone = request.POST['phone']
        profile.twitter = request.POST['twitter']
        profile.facebook = request.POST['facebook']
        profile.instagram = request.POST['instagram']
        profile.line_id = request.POST['line_id']
        profile.line_token = request.POST['line_token']
        profile.about = request.POST['about']

        profile.save()
        return HttpResponseRedirect(reverse_lazy('account:profile'))


class ChangePassword(LoginRequiredMixin, PasswordChangeView):
    model = User
    form_class = PasswordChangeForm
    template_name = 'account/change_password.html'
    success_url = reverse_lazy('login')


class MembersListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'account/members.html'
    queryset = User.objects.all().exclude(is_superuser=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Members'
        return context


class MembersDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'account/profile.html'


def sector_list(request, pk):
    qs = Profile.objects.filter(sector__pk=pk).exclude(user__is_superuser=True)
    context = {
        'object_list': qs,
        'bc_title': Sector.objects.get(pk=pk).name
    }
    return render(request, 'account/other_list.html', context)


def position_list(request, pk):
    qs = Profile.objects.filter(position__pk=pk)
    context = {
        'object_list': qs,
        'bc_title': Position.objects.get(pk=pk).name
    }
    return render(request, 'account/other_list.html', context)


class ContactView(LoginRequiredMixin, TemplateView):
    template_name = 'account/contact.html'


def check_username(request):
    username = request.GET.get('username')
    data = {
        'username_exists': User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(data)
