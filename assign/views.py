#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : views.py
# Author            : lu5her <lu5her@mail>
# Date              : Fri Oct, 28 2022, 21:12 301
# Last Modified Date: Fri Nov, 11 2022, 17:11 315
# Last Modified By  : lu5her <lu5her@mail>
from account.models import Profile
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)
from journal.models import Journal

from assign.forms import AssignForm, NoteForm, ProgressForm
from assign.models import (
    Assign,
    AssignImage,
    AssignProgress,
)

# Create your views here.


class AssignHomeView(LoginRequiredMixin, TemplateView):
    """
    AssignHomeView for Assign app

    Attributes:
        login_url:
        template_name:
    """

    # login_url = reverse_lazy("login")
    template_name = "assign/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Home"
        assign_to_user = Assign.objects.filter(assigned_to=self.request.user.profile)
        context["assign_to_user"] = assign_to_user
        context["assign_to_user_not_accepted"] = assign_to_user.filter(accepted=False)
        assign_by_user = Assign.objects.filter(author=self.request.user)
        context["assign_by_user"] = assign_by_user
        context["assign_by_user_not_accepted"] = assign_by_user.filter(accepted=False)
        context["assign_by_user_done"] = assign_by_user.filter(accepted=True)

        return context


class AssignStaffListView(LoginRequiredMixin, ListView):
    """
    AssignStaffListView for Assign app

    Attributes:
        model:
        template_name:
    """

    # login_url = reverse_lazy("login")
    model = Assign
    template_name = "assign/assign.html"
    # ordering      = ('-created_at')

    def get_queryset(self):
        qs = Assign.objects.filter(author=self.request.user)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "รายการมอบหมาย"
        return context


class AssignListView(LoginRequiredMixin, ListView):
    """
    AssignListView for Assign app

    Attributes:
        model:
        template_name:
        ordering:
    """

    # login_url = reverse_lazy("login")
    model = Assign
    template_name = "assign/assign.html"
    ordering = "-created_at"

    def get_queryset(self):
        qs = Assign.objects.filter(assigned_to=self.request.user.profile)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "รายการมอบหมาย"
        return context


class AssignDetailView(LoginRequiredMixin, DetailView):
    """
    AssignDetailView

    Attributes:
        login_url:
        template_name:
        model:
    """

    login_url = reverse_lazy("login")
    template_name = "assign/assign_detail.html"
    model = Assign

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["form"] = ProgressForm(instance=self.get_object())
        context["note_form"] = NoteForm
        context["note"] = AssignProgress.objects.filter(assign=self.object)
        context["btn_text"] = "Update"
        return context

    def post(self, request, *args, **kwargs):
        # context = self.get_context_data(object=self.get_object())
        form = ProgressForm(request.POST, instance=self.get_object())
        note_form = NoteForm(request.POST)
        if form.is_valid() and note_form.is_valid():
            note = request.POST.get("note")
            form.save()
            # check if status != DONE
            if form.cleaned_data["status"] != "Done":
                note_save = AssignProgress.objects.create(
                    assign=self.get_object(),
                    note=note,
                    status=form.cleaned_data["status"],
                )
                note_save.save()
                return HttpResponseRedirect(self.request.path_info)
            else:
                notes = []
                for note in AssignProgress.objects.filter(assign=self.get_object()):
                    notes.append(note.note)
                note_save = AssignProgress.objects.create(
                    assign=self.get_object(),
                    note=note,
                    status=form.cleaned_data["status"],
                )
                note_save.save()
                journal = Journal.objects.create(
                    author=self.request.user,
                    category=Journal.Category.SPECIAL,
                    title=self.get_object().title,
                    body=self.get_object().body + "\n\n" + "\n".join(notes),
                    status=Journal.Status.DONE,
                    header=self.get_object().author.prfile,
                )
                journal.save()
                return HttpResponseRedirect(self.request.path_info)


class AssignCreateView(LoginRequiredMixin, CreateView):
    """
    AssignCreateView for create new Assign

    Attributes:
        login_url:
        template_name:
        form_class:
        success_url:
    """

    # login_url = reverse_lazy("login")
    template_name = "assign/assign_form.html"
    form_class = AssignForm
    success_url = reverse_lazy("assign:staff-list")

    def get(self, request, *args, **kwargs):
        members = Profile.objects.all().exclude(user=self.request.user)
        context = {
            "form": self.form_class(current_user=self.request.user.profile.pk),
            "title": "Create",
            "header": "สร้างการมอบหมายงาน",
            "btn_text": "มอบหมาย",
            "members": members,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = self.form_class(request.user.profile.pk, request.POST, request.FILES)

        if form.is_valid():
            images = request.FILES.getlist("images")
            form_save = form.save()
            form_id = get_object_or_404(Assign, pk=form_save.pk)

            if images:
                for image in images:
                    a_image = AssignImage(announce=form_id, images=image)
                    a_image.save()
            else:
                form_save.save()

            # if tokens:
            # host = request.get_host()
            # path = reverse_lazy('announce:detail', args=[str(form_id.pk)])
            # url = 'http://' + host + path
            # head = '\nมี : ' + form_save.is_type.name + 'ใหม่'
            # body = '\nเรื่อง : ' + form_save.name + '\n' + 'รายละเอียดเพิ่มเติม :' + url

            # for token_id in tokens:
            # token = LineToken.objects.get(id=token_id).token
            # line = Sendline(token)
            # line.sendtext(head + body)
            # print(token)

            return redirect(self.success_url)

        else:
            form = self.form_class()

        context = {
            "form": form,
            "title": "Create",
            "header": "สร้างการมอบหมายงาน",
            "btn_text": "มอบหมาย",
        }
        return render(request, self.template_name, context)


class AssignUpdateView(LoginRequiredMixin, UpdateView):
    """
    AssignUpdateView for update Assign

    Attributes:
        template_name:
        model:
        form_class:
        pk:
    """

    # login_url = reverse_lazy("login")
    template_name = "assign/assign_form.html"
    model = Assign
    form_class = AssignForm
    pk = None
    # success_url   = reverse_lazy('assign:list')

    def get_success_url(self):
        return reverse("assign:detail", kwargs={"pk": self.get_object().pk})

    def get(self, request, *args, **kwargs):
        form = self.form_class(
            current_user=request.user.profile.pk, instance=self.get_object()
        )
        images = AssignImage.objects.filter(assign=self.get_object())

        context = {
            "form": form,
            "images": images,
            "title": "Update",
            "header": "อัพเดทการมอบหมายงาน",
            "btn_text": "อัพเดท",
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(
            request.user.profile.id,
            request.POST,
            request.FILES,
            instance=self.get_object(),
        )

        if form.is_valid():
            images = request.FILES.getlist("images")
            form_save = form.save()
            form_id = get_object_or_404(Assign, pk=form_save.pk)

            if images:
                for image in images:
                    a_image = AssignImage.objects.create(assign=form_id, images=image)
                    a_image.save()
            else:
                form_save.save()

        else:
            form = self.form_class(instance=self.get_object())

        return redirect(self.get_success_url())


class AssignNotAcceptedView(LoginRequiredMixin, ListView):
    """
    AssignNotAcceptedView for list Assign not accepted

    Attributes:
        model:
        template_name:
        ordering:
    """

    # login_url = reverse_lazy("login")
    model = Assign
    template_name = "assign/assign.html"
    # context_object_name = 'announce_list'
    ordering = "-created_at"

    def get_queryset(self):
        # return super().get_queryset()
        qs = Assign.objects.filter(~Q(author=self.request.user) & ~Q(accepted=False))
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['not_read'] = self.request.user.announce_set.filter(~Q(author=self.request.user) & Q(reads__id=self.request.user.id)).count()
        context["header"] = "ยังไม่ได้อ่าน"
        return context


class AssignDeleteView(LoginRequiredMixin, DeleteView):
    """
    AssignDeleteView for delete Assign

    Attributes:
        template_name:
        model:
        success_url:
    """

    # login_url = reverse_lazy("login")
    template_name = "assign/assign_delete.html"
    model = Assign
    success_url = reverse_lazy("assign:list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header"] = "ยืนยันการลบ"
        context["btn_text"] = "ลบ"
        return context


def accepted(request, pk):
    """
    accepted button for accepted assigned_jib
    :param request:
    :param pk:
    :return:
    """
    assigned_job = Assign.objects.get(pk=pk)
    assigned_job.accepted = True
    assigned_job.save()
    # create AssignProgress status Accepted and save
    progress = AssignProgress.objects.create(
        assign=assigned_job, status="Accepted", note="Accepted"
    )
    progress.save()
    return HttpResponseRedirect(reverse_lazy("assign:detail", args=[str(pk)]))
