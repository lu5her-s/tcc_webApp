#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : views.py
# Author            : lu5her <lu5her@mail>
# Date              : Thu Sep, 29 2022, 11:58 272
# Last Modified Date: Fri Dec, 23 2022, 18:00 357
# Last Modified By  : lu5her <lu5her@mail>
import datetime

from announce.models import (
    Announce,
    Comment,
)
from assign.models import Assign
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
from document.models import Depart, Document
from inform.models import Inform
from journal.models import Journal
from parcel.models import ParcelRequest, RequestBillDetail

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

# Create your views here.


class HomeView(LoginRequiredMixin, TemplateView):
    """
    HomeView สำหรับหน้าแรก
    แสดงผลหน้า Dashboard

    Attributes:
        template_name: str
    """

    template_name = "base.html"

    def get_context_data(self, *args, **kwargs):
        """
        get_context_data สำหรับการเรียกข้อมูลที่จะแสดงในหน้าหลัก

        Args:
            *args:
            **kwargs:

        Returns:
            context: dict

        """
        context = super().get_context_data(*args, **kwargs)
        context["announce"] = Announce.objects.all()
        context["recent_comment"] = Comment.objects.all().order_by("-created_at")[:5]
        all_inbox = Document.objects.filter(
            assigned_sector=self.request.user.profile.sector
        ).count()
        context["all_inbox"] = all_inbox
        all_department = Depart.objects.filter(
            reciever__profile__sector=self.request.user.profile.sector
        ).count()
        context["new_inbox"] = str(abs(all_inbox - all_department))
        context["journal"] = Journal.objects.filter(author=self.request.user)
        today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
        today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
        context["today_journal"] = Journal.objects.filter(
            author__profile__sector=self.request.user.profile.sector,
            created_at__range=(today_min, today_max),
        )
        try:
            context["not_read"] = Announce.objects.filter(
                ~Q(author=self.request.user) & ~Q(reads__id=self.request.user.id)
            )
        except:
            pass
        if self.request.user.groups.filter(name="Staff"):
            context["assign"] = Assign.objects.filter(author=self.request.user)
            context["wait_assign"] = Assign.objects.filter(
                author=self.request.user, accepted=False
            )
        else:
            context["assign"] = Assign.objects.filter(
                assigned_to__user=self.request.user
            )
            context["wait_assign"] = Assign.objects.filter(
                assigned_to__user=self.request.user, accepted=False
            )

        if not self.request.user.groups.filter(name="StaffRepair"):
            context["inform_department"] = Inform.objects.filter(
                customer__profile__department=self.request.user.profile.department
            )
        context["informs"] = Inform.objects.filter(
            created_at__range=(today_min, today_max)
        )
        context["wait_approve"] = Inform.objects.filter(
            Q(inform_status=Inform.InformStatus.WAIT) & Q(approve_status=None)
        )
        bills = ParcelRequest.objects.filter(user=self.request.user)
        bill_manager = ParcelRequest.objects.filter(
            Q(stock=self.request.user.profile.department)
            & ~Q(status=ParcelRequest.RequestStatus.DRAFT)
        )
        context["bill_manager"] = bill_manager
        context["request_bills"] = bills
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


def sector_list(request, sector_pk):
    """
    sector_list สำหรับการแสดงผลรายชื่อแผนก

    Args:
        request ():
        pk ():

    Returns:

    """
    profiles = Profile.objects.filter(sector__pk=sector_pk).exclude(
        user__is_superuser=True
    )
    sector = get_object_or_404(Sector, pk=sector_pk)
    # sector_name = profiles.first().sector.name
    sector_name = sector.name
    context = {"object_list": profiles, "bc_title": sector_name}
    return render(request, "account/other_list.html", context)


def position_list(request, position_pk):
    """
    position_list สำหรับการแสดงผลรายชื่อตําแหน่ง

    Args:
        request ():
        pk ():

    Returns:

    """
    qs = Profile.objects.filter(position__pk=position_pk)
    context = {"object_list": qs, "bc_title": Position.objects.get(pk=position_pk).name}
    return render(request, "account/other_list.html", context)


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
