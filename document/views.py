#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : views.py
# Author            : lu5her <lu5her@mail>
# Date              : Thu Oct, 06 2022, 23:34 279
# Last Modified Date: Mon Oct, 31 2022, 22:19 304
# Last Modified By  : lu5her <lu5her@mail>
import datetime

from account.models import Sector
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import HttpResponseRedirect, redirect, render, reverse
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)

from document.forms import DocumentForm
from document.models import Depart, Document

# Create your views here.


class DocumentHomeView(LoginRequiredMixin, TemplateView):
    """DocumentHomeView."""

    template_name = "document/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["inbox"] = Document.objects.filter(
            assigned_sector=self.request.user.profile.sector
        )
        # context['not_accept'] =
        context["outbox"] = Document.objects.filter(
            author__profile__sector=self.request.user.profile.sector
        )
        # context['new_inbox'] = Department.objects.filter(recieved=False)
        all_inbox = Document.objects.filter(
            assigned_sector=self.request.user.profile.sector
        ).count()
        all_department = Depart.objects.filter(
            reciever__profile__sector=self.request.user.profile.sector
        ).count()
        context["new_inbox"] = str(abs(all_inbox - all_department))

        today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
        today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
        context["today_outbox"] = Document.objects.filter(
            author__profile__sector=self.request.user.profile.sector,
            created_at__range=(today_min, today_max),
        )
        return context


class DocumentCreateView(LoginRequiredMixin, CreateView):
    """
    DocumentCreateView for create new Document

    Attributes:
        model:
        form_class:
        template_name:
        success_url:
    """

    model = Document
    form_class = DocumentForm
    template_name = "document/create_form.html"
    # template_name = 'document/forms.html'
    success_url = reverse_lazy("document:outbox")

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        context = {
            "form": form,
            "header": "สร้างเอกสาร",
            "bc_title": "Document",
        }
        return render(self.request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)

        if form.is_valid():
            form_save = form.save(commit=False)
            form_save.author = self.request.user
            form_save.save()
            for s in self.request.POST.getlist("assigned_sector"):
                sector = Sector.objects.get(pk=s)
                form_save.assigned_sector.add(sector)
            return redirect(self.success_url)
        else:
            form = self.form_class
            return render(request, self.template_name, context={"form": form})


class InboxListView(LoginRequiredMixin, ListView):
    """
    InboxListView for Document app

    Attributes:
        model:
        template_name:
    """

    model = Document
    template_name = "document/inbox.html"

    def get_queryset(self):
        qs = Document.objects.filter(
            assigned_sector=self.request.user.profile.sector, is_deleted=False
        )
        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context["title"] = "กล่องขาเข้า"
        # pk_list = Department.objects.all().sector_set.filter(name=self.request.user.profile.sector.name).values_list('reciever__profile__sector', flat=True)
        pk_list = Depart.objects.filter(
            reciever__profile__sector=self.request.user.profile.sector
        ).values_list("document__pk", flat=True)
        # pk_list = Department.objects.filter(reciever__profile__sector = self.request.user.profile.sector)
        context["all_accepted"] = pk_list

        return context


class InboxDetailView(LoginRequiredMixin, DetailView):
    """InboxDetailView.
    show detail document and acceptable in page
    """

    model = Document
    template_name = "document/inbox_detail.html"

    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        context = super().get_context_data(**kwargs)
        context["department"] = Document.objects.get(pk=self.object.pk).depart_set.all()
        try:
            d = Depart.objects.get(
                document=self.object,
                reciever__profile__sector=self.request.user.profile.sector,
            )
            context["accepted"] = d
        except:
            context["accepted"] = None
        return context


class OutboxListView(LoginRequiredMixin, ListView):
    """
    OutboxListView for Document appOutboxListView for Document app

    Attributes:
        model:
        template_name:
    """

    model = Document
    template_name = "document/outbox.html"

    def get_queryset(self):
        qs = Document.objects.filter(
            author__profile__sector=self.request.user.profile.sector
        )
        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context["title"] = "กล่องขาออก"
        return context


class OutboxDetailView(LoginRequiredMixin, DetailView):
    """
    OutboxDetailView for detail Document

    Attributes:
        model:
        template_name:
    """

    model = Document
    template_name = "document/outbox_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            # d =  Document.objects.get(pk=self.get_object().pk).department_set.all().values_list('reciever__profile__sector', flat=True)
            d = Document.objects.get(pk=self.get_object().pk).department_set.get(
                reciever__profile__sector=self.request.user.profile.sector
            )
            context["accepted"] = d
        except:
            context["accepted"] = None
        context["all_accepted"] = (
            Document.objects.get(pk=self.get_object().pk)
            .depart_set.all()
            .values_list("reciever__profile__sector__pk", flat=True)
        )
        context["accept_detail"] = Depart.objects.filter(document=self.get_object())
        return context


class DocumentUpdateView(LoginRequiredMixin, UpdateView):
    """
    DocumentUpdateView for update Document

    Attributes:
        template_name:
        model:
        form_class:
        success_url:
        object:
        object:
    """

    template_name = "document/update_form.html"
    model = Document
    form_class = DocumentForm
    success_url = reverse_lazy("document:outbox")

    def get_success_url(self):
        return reverse("document:outbox-detail", kwargs={"pk": self.pk})

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(instance=self.object)

        context = {
            "form": form,
            "title": "Update",
            "header": "แก้ไขเอกสาร",
        }
        return render(request, self.template, context)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(requst.POST, request.FILES, instance=self.object)

        if form.is_valid():
            form_save = form.save(commit=False)
            form_save.author = self.request.user
            form_save.save()
            for s in self.request.POST.getlist("assigned_sector"):
                sector = Sector.objects.get(pk=s)
                form_save.assigned_sector.add(sector)
            return redirect(self.success_url)
        else:
            form = self.form_class
            return render(request, self.template_name, context={"form": form})


class DocumentDelete(LoginRequiredMixin, DeleteView):
    """
    DocumentDelete for delete Document

    Attributes:
        login_url:
        template_name:
        model:
        success_url:
        object:
    """

    login_url = reverse_lazy("login")
    template_name = "document/delete.html"
    model = Document
    success_url = reverse_lazy("document:outbox")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header"] = "ยืนยันการลบ"
        context["btn_text"] = "ลบ"
        return context

    # def get_success_url(self):
    # return reverse_lazy('announce:list')

    def post(self, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            self.object.is_delete = True
            self.object.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super().post(s * args, **kwargs)


def accept_document(request, pk):
    """
    accept_document for accept document

    Args:
        request ():
        pk ():

    Returns:

    """
    document = Document.objects.get(pk=pk)
    # reciever = request.user
    department = Depart.objects.create(
        document=document,
        reciever=request.user,
    )
    department.save()
    return HttpResponseRedirect(reverse_lazy("document:inbox-detail", args=[str(pk)]))
