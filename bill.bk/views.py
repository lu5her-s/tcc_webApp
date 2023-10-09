from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import ListView, TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin

from bill.models import RequestBill
from bill.forms import SelectDepartmentForm
from account.models import Department

# Create your views here.

class BillHomeView(LoginRequiredMixin, TemplateView):
    template_name = 'bill/bill_home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class BillListView(LoginRequiredMixin, ListView):
    model = RequestBill
    template_name = 'bill/bill_home.html'


class SelectDepartmentView(LoginRequiredMixin, View):
    form_class = SelectDepartmentForm
    template_name = 'bill/select_department.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            department_id = form.cleaned_data['department']
            department = get_object_or_404(Department, pk=department_id)
            return redirect('bill:request_bill_create', department.pk)
        return render(request, self.template_name, {'form': form})


class RequestBillCreateView(LoginRequiredMixin, View):
    template_name = 'bill/bill_create.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
