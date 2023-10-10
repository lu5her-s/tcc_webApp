from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView, TemplateView

from .models import RequestBill

# Create your views here.

class ParcelHomeView(LoginRequiredMixin, TemplateView):
    template_name = 'parcel/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_bill'] = 'Test all_bill'
        context['wait_approve'] = 'Test wait_approve'
        context['parcel_list'] = 'Test parcel_list'
        context['on_hand'] = 'Test on_hand'
        return context


class BillListView(LoginRequiredMixin, ListView):
    template_name = 'parcel/bill_list.html'
    model = RequestBill

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'รายการใบเบิก'
        return context


class BillDetailView(LoginRequiredMixin, DetailView):
    template_name = 'parcel/bill_detail.html'
    model = RequestBill

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bill_detail'] = RequestBillDetail.objects.filter(bill=self.get_object())
        context['bill_items'] = RequestItem.objects.filter(bill=self.get_object())
        return context
