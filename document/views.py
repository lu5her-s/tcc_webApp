#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : views.py
# Author            : lu5her <lu5her@mail>
# Date              : Thu Oct, 06 2022, 23:34 279
# Last Modified Date: Fri Oct, 21 2022, 00:16 294
# Last Modified By  : lu5her <lu5her@mail>
import datetime
from django.contrib.auth.mixins         import LoginRequiredMixin
from django.contrib.contenttypes.models import Q
from django.shortcuts                   import redirect, render
from django.urls import reverse_lazy
from django.views.generic               import (
    DetailView,
    ListView,
    TemplateView,
    CreateView,
)
from account.models import Sector
from document.models import Document, Department
from document.forms  import DocumentForm

# Create your views here.

class DocumentHomeView(LoginRequiredMixin, TemplateView):
    """DocumentHomeView."""

    template_name = 'document/home.html'

    def get_context_data(self, **kwargs):
        context                = super().get_context_data(**kwargs)
        context['inbox']       = Document.objects.filter(assigned_sector = self.request.user.profile.sector)
        context['outbox']      = Document.objects.filter(author__profile__sector = self.request.user.profile.sector)
        # context['new_inbox'] = Department.objects.filter(recieved=False)
        all_inbox              = Document.objects.filter(assigned_sector = self.request.user.profile.sector).count()
        all_department         = Department.objects.filter(reciever__profile__sector = self.request.user.profile.sector).count()
        context['new_inbox']   = str(all_inbox - all_department)

        today_min               = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
        today_max               = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
        context['today_outbox'] = Document.objects.filter(
            author__profile__sector = self.request.user.profile.sector,
            created_at__range=(today_min, today_max)
        )
        return context

class DocumentCreateView(LoginRequiredMixin, CreateView):
    model         = Document
    form_class    = DocumentForm
    template_name = 'document/create_form.html'
    # template_name = 'document/forms.html'
    success_url = reverse_lazy('document:outbox')

    def get(self, request, *args, **kwargs):
        form    = self.form_class()
        context = {
            'form': form,
            'header': 'สร้างเอกสาร',
            'bc_title': 'Document',
        }
        return render(self.request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)

        if form.is_valid():
            form_save        = form.save(commit=False)
            form_save.author = self.request.user
            form_save.save()
            for s in self.request.POST.getlist('assigned_sector'):
                sector = Sector.objects.get(pk=s)
                form_save.assigned_sector.add(sector)
            return redirect(self.success_url)
        else:
            form = self.form_class
            return render(request, self.template_name, context={'form': form})


class InboxListView(LoginRequiredMixin, ListView):
    model = Document
    template_name = 'document/inbox.html'

    def get_queryset(self):
        qs = Document.objects.filter(assigned_sector = self.request.user.profile.sector)
        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['title'] = 'กล่องขาเข้า'
        return context

class InboxDetailView(LoginRequiredMixin, DetailView):
    """InboxDetailView.
    show detail document and acceptable in page
    """
    model = Document
    template_name = 'document/inbox_detail.html'

class OutboxListView(LoginRequiredMixin, ListView):
    model = Document
    template_name = 'document/outbox.html'

    def get_queryset(self):
        qs = Document.objects.filter(author__profile__sector = self.request.user.profile.sector)
        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['title'] = 'กล่องขาออก'
        return context
