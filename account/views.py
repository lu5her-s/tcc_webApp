#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : views.py
# Author            : lu5her <lu5her@mail>
# Date              : Thu Sep, 29 2022, 11:58 272
# Last Modified Date: Tue May, 27 2025, 13:43 147
# Last Modified By  : lu5her <lu5her@mail>
import datetime

from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView
from django.contrib.contenttypes.models import Q
from django.http import JsonResponse
from django.shortcuts import HttpResponseRedirect, get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    TemplateView,
)
from .helpers import (
    get_inbox_counts,
    get_journals,
    get_not_read_announces,
    get_today_range,
)

from account.forms import (
    ProfileForm,
    UserForm,
)
from account.models import Department as DP
from account.models import (
    Position,
    Profile,
    Rank,
    Sector,
)
from announce.models import (
    Announce,
    Comment,
)
from assign.models import Assign
from document.models import Depart, Document
from inform.models import Inform
from journal.models import Journal
from parcel.models import ParcelRequest, RequestBillDetail

# Create your views here.


class HomeView(LoginRequiredMixin, TemplateView):
    """
    HomeView สำหรับหน้าแรก
    แสดงผลหน้า Dashboard

    Attributes:
        template_name: str
    """

    template_name = "base.html"

    def get_context_data(self, **kwargs):
        """
        get_context_data สำหรับการเรียกข้อมูลที่จะแสดงในหน้าหลัก

        Args:
            *args:
            **kwargs:

        Returns:
            context: dict

        """
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Fetch data via helper functions
        context["announce"] = Announce.objects.all()
        context["recent_comment"] = Comment.objects.all().order_by("-created_at")[:5]

        # Inbox counts
        all_inbox, all_department, new_inbox = get_inbox_counts(user)
        context.update(
            {
                "all_inbox": all_inbox,
                "new_inbox": new_inbox,
            }
        )

        # Journals
        context["journal"] = Journal.objects.filter(author=user)
        context["today_journal"] = get_journals(user)

        # Announce unread
        context["not_read"] = get_not_read_announces(user)

        # Assigns bases on group
        if self.request.user.groups.filter(name="Staff").exists():
            context["assign"] = Assign.objects.filter(author=user)
            context["wait_assign"] = Assign.objects.filter(author=user, accepted=False)
        else:
            context["assign"] = Assign.objects.filter(assigned_to__user=user)
            context["wait_assign"] = Assign.objects.filter(
                assigned_to__user=user, accepted=False
            )

        # Inform department
        if not self.request.user.groups.filter(name="StaffRepair").exists():
            context["inform_department"] = Inform.objects.filter(
                customer__profile__department=user.profile.department
            )

        # Inform and bills
        today_min, today_max = get_today_range()
        context["informs"] = Inform.objects.filter(
            created_at__range=(today_min, today_max)
        )
        context["wait_approve"] = Inform.objects.filter(
            inform_status=Inform.InformStatus.WAIT, approve_status=None
        )

        # all_department = Depart.objects.filter(
        #     reciever__profile__sector=self.request.user.profile.sector
        # ).count()
        context["new_inbox"] = str(abs(all_inbox - all_department))
        today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
        today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)

        bills = ParcelRequest.objects.filter(user=user)
        context["request_bills"] = bills
        context["bill_manager"] = ParcelRequest.objects.filter(
            stock=user.profile.department
        ).exclude(status=ParcelRequest.RequestStatus.DRAFT)

        context["bill_wait_approve"] = bills.filter(
            billdetail__approve_status=RequestBillDetail.ApproveStatus.WAIT
        )
        return context


class RegisterView(CreateView):
    """
    RegisterView สำหรับการสมัครสมาชิกใหม่

    Attributes:
        form_class: Instance of UserCreationForm
        model: Instance of User
        template_name: str
        success_url: str -> return to login page
    """

    form_class = UserForm
    model = User
    template_name = "account/register.html"
    success_url = reverse_lazy("login")


class ProfileView(LoginRequiredMixin, TemplateView):
    """
    ProfileView สำหรับการแสดงผลของผู้ใช้
    รายละเอียดของผู้ใช้ และการเปลี่ยนรหัสผ่าน

    Attributes:
        model: Instance of User
        template_name: str
    """

    model = User
    template_name = "account/profile.html"

    def get_context_data(self, **kwargs):
        """
        get_context_data สำหรับการเรียกข้อมูลที่จะแสดง

        Args:
            **kwargs:

        Returns:

        """
        context = super().get_context_data(**kwargs)
        context["user_form"] = UserForm(instance=self.request.user)
        context["profile_form"] = ProfileForm(instance=self.request.user.profile)
        context["password_form"] = PasswordChangeForm(self.request.user)
        return context


def update_profile(request):
    """
    function สำหรับการเปลี่ยนข้อมูลผู้ใช้

    Args:
        request ():

    Returns:
        HttpResponseRedirect:

    """
    user = get_object_or_404(User, pk=request.user.pk)
    profile = get_object_or_404(Profile, user=user)

    if request.method == "POST":
        user.first_name = request.POST["first_name"]
        user.last_name = request.POST["last_name"]
        user.email = request.POST["email"]

        user.save()

        if request.FILES:
            profile.image = request.FILES.get("image")

        if request.POST["rank"]:
            rank = request.POST["rank"]
            profile.rank = Rank.objects.get(pk=rank)

        if request.POST["position"]:
            profile.position = Position.objects.get(pk=request.POST["position"])

        if request.POST["sector"]:
            profile.sector = Sector.objects.get(pk=request.POST["sector"])

        # profile.place      = request.POST['place']
        if request.POST["department"]:
            profile.department = DP.objects.get(pk=request.POST["department"])

        profile.address = request.POST["address"]
        profile.phone = request.POST["phone"]
        profile.twitter = request.POST["twitter"]
        profile.facebook = request.POST["facebook"]
        profile.instagram = request.POST["instagram"]
        profile.line_id = request.POST["line_id"]
        profile.line_token = request.POST["line_token"]
        profile.about = request.POST["about"]

        profile.save()
        return HttpResponseRedirect(reverse_lazy("account:profile"))


class ChangePassword(LoginRequiredMixin, PasswordChangeView):
    """
    ChangePassword สำหรับการเปลี่ยนรหัสผ่าน

    Attributes:
        model:
        form_class:
        template_name:
        success_url: return to login page
    """

    model = User
    form_class = PasswordChangeForm
    template_name = "account/change_password.html"
    success_url = reverse_lazy("login")


class MembersListView(LoginRequiredMixin, ListView):
    """
    MembersListView สำหรับการแสดงผลราบชื่อชองสมาชิก

    Attributes:
        model:
        template_name: account/members.html
    """

    model = Profile
    template_name = "account/members.html"
    context_object_name = "members"

    def get_queryset(self):
        """
        get_queryset สำหรับการเรียกข้อมูลรายชื่อชองสมาชิก

        Returns:

        """
        # all profile exclude is_superuser
        return Profile.objects.exclude(user__is_superuser=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Members"
        return context


class MembersDetailView(LoginRequiredMixin, DetailView):
    """
    MembersDetailView สำหรับการแสดงผลรายชื่อชองสมาชิก

    Attributes:
        model:
        template_name:
    """

    model = User
    template_name = "account/profile.html"


class ProfileListView(LoginRequiredMixin, ListView):
    """
    ProfileListView สำหรับการแสดงผลรายชื่อผู้ใช้ที่มีชื่อแผนกหรือตําแหน่ง

    Attributes:
        model:
        template_name:
    """

    model = Profile
    template_name = "account/other_list.html"

    def get_queryset(self):
        filter_type = self.kwargs.get("filter_type")
        pk = self.kwargs.get("pk")
        if filter_type == "sector":
            return Profile.objects.filter(sector__pk=pk).exclude(
                user__is_superuser=True
            )
        elif filter_type == "position":
            return Profile.objects.filter(position__pk=pk).exclude(
                user__is_superuser=True
            )
        return Profile.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        filter_type = self.kwargs.get("filter_type")
        pk = self.kwargs.get("pk")
        if filter_type == "sector":
            sector = get_object_or_404(Sector, pk=pk)
            context["bc_title"] = sector.name
        elif filter_type == "position":
            position = get_object_or_404(Position, pk=pk)
            context["bc_title"] = position.name
        return context


class ContactView(LoginRequiredMixin, TemplateView):
    template_name = "account/contact.html"


def check_username(request):
    """
    check_username สำหรับการตรวจสอบชื่อผู้ใช้
    สำหรับการลงทะเบียน

    Args:
        request ():

    Returns:

    """
    username = request.GET.get("username")
    data = {"username_exists": User.objects.filter(username__iexact=username).exists()}
    return JsonResponse(data)
