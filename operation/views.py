#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : views.py
# Author            : lu5her <lu5her@mail>
# Date              : Sun Jun, 30 2024, 16:53 182
# Last Modified Date: Fri Nov, 08 2024, 21:03 313
# Last Modified By  : lu5her <lu5her@mail>
# -----
import os

from account.models import Department
from car.forms import CarReturnForm
from car.models import CarBooking
from config.utils import generate_pdf

# for  get media path
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, Q
from django.shortcuts import HttpResponse, get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, TemplateView, View
from inform.models import Inform
from parcel.models import ParcelRequest

from .forms import (
    AddFuelForm,
    AddInformForm,
    CarAddForm,
    OperationForm,
    OperationParcelRequestForm,
    OperationParcelReturnForm,
    TaskForm,
    TaskNoteForm,
    TeamForm,
    TeamMemberFormSet,
)
from .models import (
    Allowance,
    AllowanceRefund,
    AllowanceWithdraw,
    OilReimburesment,
    Operation,
    OperationCar,
    OperationInform,
    OperationParcelRequest,
    OperationParcelReturn,
    Task,
    Team,
    TeamMember,
)

# Create your views here.


class OperationHome(LoginRequiredMixin, TemplateView):
    """
    Home Operation แสดงหน้าหลักของใบงาน

    Attributes:
        template_name: operation/index.html
    """

    template_name = "operation/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_operation = Operation.objects.filter(~Q(operation_status="DF"))
        user_all_operation = Operation.objects.filter(
            team__members__member=self.request.user
        )
        context["user_operation_all"] = user_all_operation
        context["user_operation_draft"] = user_all_operation.filter(
            operation_status="DF"
        )
        context["user_wait_approve"] = user_all_operation.filter(approve_status="WO")
        context["operation_on_progress"] = user_all_operation.filter(
            operation_status="IP"
        )
        context["user_operation_done"] = user_all_operation.filter(
            operation_status="DO"
        )
        context["user_wait_close"] = user_all_operation.filter(operation_status="WC")
        # For command Home
        context["command_overview"] = all_operation
        context["wait_approve_open"] = all_operation.filter(approve_status="WO")
        context["wait_approve_close"] = all_operation.filter(approve_status="WC")
        return context


class OperationCreateView(LoginRequiredMixin, View):
    """
    Create new Operation

    Attributes:
        template_name:
    """

    template_name = "operation/operation_form.html"

    def get(self, request):
        context = {
            "operation_form": OperationForm,
            "team_form": TeamForm,
        }
        return render(request, self.template_name, context=context)

    def post(self, request):
        operation_form = OperationForm(request.POST)
        team_form = TeamForm(request.POST)
        if operation_form.is_valid() and team_form.is_valid():
            operation_form_data = operation_form.cleaned_data
            if operation_form_data["type_of_work"] == "OT":
                other_type = request.POST.get("other_type")
                self.object = operation_form.save(commit=False)
                self.object.other_type = other_type
                self.object.created_by = self.request.user
                self.object.save()
            else:
                self.object = operation_form.save(commit=False)
                self.object.created_by = self.request.user
                self.object.save()
            team = team_form.save(commit=False)
            team.operation = self.object
            if self.object.created_by == team.team_leader:
                team.accept()
            team.save()

            return redirect(
                reverse_lazy("operation:detail", kwargs={"pk": self.object.pk})
            )
        else:
            return render(
                request, self.template_name, context={"operation_form": operation_form}
            )


class OperationDetailView(LoginRequiredMixin, DetailView):
    """
    Detail View for Operation

    Attributes:
        model: operation and other on this app
        template_name:
        object:
    """

    model = Operation
    template_name = "operation/operation_detail.html"

    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        team = Team.objects.get(operation=self.object)
        context = {
            "object": self.object,
            "team": team,
            "tasks": Task.objects.filter(operation=self.object),
            "task_form": TaskForm,
            "members": TeamMember.objects.filter(team=team),
            "team_member_formset": TeamMemberFormSet,
            "cars": OperationCar.objects.filter(operation=self.object),
            "operation_form": OperationForm,
            "car_add_form": CarAddForm,
            "car_return_form": CarReturnForm,
            "oil_request": self.object.oil_request.all()
            .values("oil_type")
            .annotate(total_liters=Sum("liter_request"))
            .order_by("oil_type"),
            "add_fuel_form": AddFuelForm,
            # for operation request and retunr parcel
            "parcel_requests": self.object.parcel_requests.all(),
            "parcel_returns": self.object.parcel_returns.all(),
            "parcel_request_form": OperationParcelRequestForm,
            "parcel_return_form": OperationParcelReturnForm,
            # for note form
            "note_form": TaskNoteForm,
            # for allowance
            "allowances": AllowanceWithdraw.objects.filter(
                allowance__operation=self.object
            ),
            "inform_add_form": AddInformForm,
        }
        return context


class OperationMemberListView(LoginRequiredMixin, ListView):
    """
    แสดงรายการใบงานตาม User

    Attributes:
        template_name:
    """

    template_name = "operation/operation_member_list.html"

    def get_queryset(self):
        operations = Operation.objects.filter(team__members__member=self.request.user)
        return operations


class OperationCommandWaitOpenListView(LoginRequiredMixin, ListView):
    """
    List all Operation for command

    Attributes:
        template_name:
    """

    template_name = "operation/operation_list.html"

    def get_queryset(self):
        operations = Operation.objects.filter(~Q(operation_status="DF"))
        return operations

    def get_context_data(self, *, object_list=None, **kwargs):
        object_list = self.get_queryset()
        context = super().get_context_data(object_list=object_list, **kwargs)
        context["object_list"] = object_list.filter(approve_status="WO")
        context["title"] = "รายการรออนุมัติเปิดงาน"
        return context


class OperationCommandWaitCloseListView(LoginRequiredMixin, ListView):
    """
    List all Operation for command

    Attributes:
        template_name:
    """

    template_name = "operation/operation_list.html"

    def get_queryset(self):
        operations = Operation.objects.filter(~Q(operation_status="DF"))
        return operations

    def get_context_data(self, *, object_list=None, **kwargs):
        object_list = self.get_queryset()
        context = super().get_context_data(object_list=object_list, **kwargs)
        context["object_list"] = object_list.filter(approve_status="WC")
        context["title"] = "รายการรออนุมัติปิดงาน"
        return context


class OperationCommandOverviewListView(LoginRequiredMixin, ListView):
    """
    List all Operation for command_overview

    Attributes:
        template_name:
    """

    template_name = "operation/operation_list.html"

    def get_queryset(self):
        operations = Operation.objects.filter(~Q(operation_status="DF"))
        return operations

    def get_context_data(self, *, object_list=None, **kwargs):
        object_list = self.get_queryset()
        context = super().get_context_data(object_list=object_list, **kwargs)
        context["object_list"] = object_list
        context["title"] = "รายการงานทั้งหมด"
        return context


class OperationOverviewTemplateView(LoginRequiredMixin, TemplateView):
    """
    แสดงรายการใบงานทั้งหมด

    Attributes:
        template_name:
    """

    template_name = "operation/overview.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        operations = Operation.objects.filter(~Q(operation_status="DF"))
        context["operations"] = operations
        context["pendings"] = operations.filter(
            Q(approve_status="WO") | Q(approve_status="WC")
        )
        context["opens"] = operations.filter(approve_status="AP")
        context["closes"] = operations.filter(approve_status="CL")
        context["relay_stock"] = operation.filter(
            parcel_requests__stock_control="คลังวิทยุถ่ายทอด"
        )
        return context


def accept_leader(request, pk):
    """
    Leader Accept Operation

    Args:
        request ():
        pk ():

    Returns:

    """
    if request.method == "POST":
        team = Team.objects.get(pk=pk)
        team.accept()
        team.save()
        return redirect(
            reverse_lazy("operation:detail", kwargs={"pk": team.operation.pk})
        )


# WARN: check user exist
def team_member_create(request, pk):
    """
    สร้างสมาชิกของชุด

    Args:
        request ():
        pk ():

    Returns:

    """
    team = Team.objects.get(pk=pk)
    form_set = TeamMemberFormSet(request.POST)
    if form_set.is_valid():
        for form in form_set:
            member = form.cleaned_data.get("member")
            if member.pk not in team.members.values_list("member", flat=True):
                TeamMember.objects.create(team=team, member=member)
                # print("Already exist")
    else:
        print(form_set.errors)
    return redirect(reverse_lazy("operation:detail", kwargs={"pk": team.operation.pk}))


def delete_team_member(request, pk):
    if request.method == "POST":
        team_member = TeamMember.objects.get(pk=pk)
        team_member.delete()
        return redirect(
            reverse_lazy(
                "operation:detail", kwargs={"pk": team_member.team.operation.pk}
            )
        )


def update_operation_date(request, pk):
    if request.method == "POST":
        operation = Operation.objects.get(pk=pk)
        # print(operation.start_date)
        # print("======")
        # print(request.POST.get("start_date"))
        operation.start_date = (
            request.POST.get("start_date")
            if request.POST.get("start_date")
            else operation.start_date
        )
        operation.end_date = (
            request.POST.get("end_date")
            if request.POST.get("end_date")
            else operation.end_date
        )
        operation.save()
        return redirect(reverse_lazy("operation:detail", kwargs={"pk": pk}))


# car operation
def car_operation_add(request, pk):
    # form = CarAddForm(request.POST)
    if request.method == "POST":
        data = request.POST
        operation = Operation.objects.get(pk=pk)
        operation.own_car = False
        operation.save()
        car_booking = int(data.get("car_booking"))
        # print(car_booking)
        # print(operation.cars.values_list("car_booking", flat=True))
        # print(
        #     car_booking
        #     not in list(operation.cars.values_list("car_booking", flat=True))
        # )
        if car_booking not in list(
            operation.cars.values_list("car_booking", flat=True)
        ):
            OperationCar.objects.create(
                operation=operation,
                car_booking=CarBooking.objects.get(pk=data.get("car_booking")),
            )
            # print("in if statement")
        # print(f"{data}  for -- operation no {operation}")
    return redirect(reverse_lazy("operation:detail", kwargs={"pk": pk}))


def change_car(request, pk):
    """
    Change car to own_car

    Args:
        request ():
        pk ():

    Returns:

    """
    if request.method == "POST":
        operation = Operation.objects.get(pk=pk)
        operation.own_car = True
        operation.cars.all().delete()
        operation.save()
    return redirect(reverse_lazy("operation:detail", kwargs={"pk": pk}))


def delete_car(request, pk):
    """
    Delete car from operation.

    Args:
        request (): The HTTP request object.
        pk (): The primary key of the operation car to delete.

    Returns:
        A redirect to the operation detail page.
    """
    if request.method == "POST":
        car = OperationCar.objects.get(pk=pk)
        operation = car.operation
        car.delete()
        # check if operation has no car change to own_car
        if not OperationCar.objects.filter(operation=operation).exists():
            operation.own_car = True
            operation.save()

        return redirect(reverse_lazy("operation:detail", kwargs={"pk": pk}))


# for request fuel
def request_fuel(request, pk):
    """
    for add fuel to operation

    Args:
        request ():
        pk ():

    Returns:

    """
    if request.method == "POST":
        operation = Operation.objects.get(pk=pk)
        # operation.oil_request.add(
        #     OilRequest.objects.get(pk=request.POST.get("oil_request"))
        # )
        data = request.POST
        # print("Diesel : ", float(data.get("diesel")))
        # print("Benzine: ", float(data.get("benzine")))
        # print(type(data.get("diesel")))
        # print(data)
        # print(operation)
        if data.get("diesel") != 0.0:
            operation.oil_request.create(
                oil_type=OilReimburesment.OilType.DIESEL,
                liter_request=data.get("diesel"),
                created_by=request.user,
                operaion=operation,
            )
        if data.get("benzine") != 0.0:
            operation.oil_request.create(
                oil_type=OilReimburesment.OilType.BENZENE,
                liter_request=data.get("benzine"),
                created_by=request.user,
                operaion=operation,
            )
    return redirect(reverse_lazy("operation:detail", kwargs={"pk": pk}))


def edit_fuel(request, pk):
    """
    Update requested fuel for an operation.

    Args:
        request: The HTTP request object.
        pk: The primary key of the operation.

    Returns:
        A redirect to the operation detail view.
    """
    if request.method == "POST":
        data = request.POST
        for oil in data.getlist("oil_request_pk"):
            oil_request = OilReimburesment.objects.get(pk=oil)
            oil_edit = data.get(f"oil_{oil}")
            oil_request.liter_request = float(oil_edit)
            oil_request.save()
        return redirect(reverse_lazy("operation:detail", kwargs={"pk": pk}))


def delete_fuel_request(request, pk):
    """
    Delete a fuel request from an operation.

    Args:
        request: The HTTP request object.
        pk: The primary key of the operation.

    Returns:
        A redirect to the operation detail view.
    """
    if request.method == "POST":
        oil_request = OilReimburesment.objects.get(pk=pk)
        operation = oil_request.operaion
        oil_request.delete()
        return redirect(reverse_lazy("operation:detail", kwargs={"pk": operation.pk}))


# Operation Task save
def operation_task_add(request, pk):
    """
    Add a task to the given operation.

    Args:
        request: The HTTP request object.
        pk: The primary key of the operation to add the task to.

    Returns:
        A redirect to the operation detail page.
    """
    if request.method == "POST":
        operation = Operation.objects.get(pk=pk)
        data = request.POST
        # print(data)
        Task.objects.create(
            operation=operation,
            workplace=Department.objects.get(pk=data.get("workplace")),
            priority=data.get("priority"),
            task=data.get("task"),
            created_by=request.user,
        )
    return redirect(reverse_lazy("operation:detail", kwargs={"pk": pk}))


def operation_task_delete(request, pk):
    """
    Delete a task from the given operation.

    Args:
        request: The HTTP request object.
        pk: The primary key of the operation to delete the task from.

    Returns:
        A redirect to the operation detail page.
    """
    if request.method == "POST":
        task_id = request.POST.get("task_delete")
        if task_id:
            task = get_object_or_404(Task, pk=task_id)
            task.delete()
    return redirect(reverse_lazy("operation:detail", kwargs={"pk": pk}))


def operation_note_add(request, pk):
    """
    จัดการการเพิ่มโน้ตไปยังงานและปิดการดำเนินการ

    Args:
        request: The HTTP request object.
        pk: The primary key of the operation.

    Returns:
        A redirect to the operation detail page.
    """
    if request.method == "POST":
        operation = Operation.objects.get(pk=pk)
        data = request.POST
        # task = Task.objects.get(pk=data.get("task"))
        if data.get("status") == "CL":
            operation.close()
    return redirect(reverse_lazy("operation:detail", kwargs={"pk": operation.pk}))


# for allowance handle
def allowance_add(request, pk):
    if request.method == "POST":
        operation = Operation.objects.get(pk=pk)
        data = request.POST
        allowance, _ = Allowance.objects.get_or_create(
            operation=operation, user=request.user
        )
        withdraw = AllowanceWithdraw.objects.create(
            allowance=allowance,
            amount=float(data.get("amount")),
            note=data.get("allowance_note"),
        )
        allowance.add_total_withdraw(float(data.get("amount")))
        allowance.increase_number_of_withdraw()
        allowance.save()
        withdraw.save()
        return redirect(reverse_lazy("operation:detail", kwargs={"pk": pk}))


def allowance_delete(request, pk):
    if request.method == "POST":
        # get allowance_withdraw pk from POST
        allowance_withdraw = AllowanceWithdraw.objects.get(pk=pk)
        operation = allowance_withdraw.allowance.operation
        allowance = allowance_withdraw.allowance
        # calculate total withdraw and decrease number of withdraw
        allowance.decrease_total_withdraw(float(allowance_withdraw.amount))
        allowance.decrease_number_of_withdraw()
        allowance_withdraw.delete()
        # if allowance.number_of_withdraw == 0:
        #     allowance.delete()
        allowance.save()
        return redirect(reverse_lazy("operation:detail", kwargs={"pk": operation.pk}))


def allowance_refund(request, pk):
    """
    Create a new allowance refund for the given operation.

    Args:
        request: The HTTP request object.
        pk: The primary key of the operation.

    Returns:
        A redirect to the operation detail page.
    """
    if request.method == "POST":
        operation = Operation.objects.get(pk=pk)
        data = request.POST
        allowance = operation.allowance
        refund = AllowanceRefund.objects.create(
            allowance=allowance,
            refund_amount=float(data.get("refund_amount")),
            note=data.get("refund_note"),
        )
        refund.save()
        return redirect(reverse_lazy("operation:detail", kwargs={"pk": pk}))


def allowance_refund_update(request, pk):
    """
    Update an existing allowance refund.

    Args:
        request: The HTTP request object.
        pk: The primary key of the allowance refund to update.

    Returns:
        A redirect to the operation detail page.
    """
    if request.method == "POST":
        allowance_refund = AllowanceRefund.objects.get(pk=pk)
        data = request.POST
        allowance_refund.amount = float(data.get("refund_amount"))
        allowance_refund.note = data.get("refund_note")
        allowance_refund.save()
        return redirect(
            reverse_lazy(
                "operation:detail",
                kwargs={"pk": allowance_refund.allowance.operation.pk},
            )
        )


def allowance_refund_delete(request, pk):
    """
    Delete an existing allowance refund.

    Args:
        request: The HTTP request object.
        pk: The primary key of the allowance refund to delete.

    Returns:
        A redirect to the operation detail page.
    """
    if request.method == "POST":
        allowance_refund = AllowanceRefund.objects.get(pk=pk)
        operation = allowance_refund.allowance.operation
        allowance_refund.delete()
        return redirect(reverse_lazy("operation:detail", kwargs={"pk": operation.pk}))


def parcel_requests_add(request, pk):
    """
    Add parcel requests to the operation.

    Args:
        request (): The HTTP request object.
        pk (): The primary key of the operation.

    Returns:
        A redirect to the operation detail page.
    """
    # TODO: edit save parcel request
    if request.method == "POST":
        operation = Operation.objects.get(pk=pk)
        data = request.POST
        parcel_request = int(data.get("parcel_request"))
        if parcel_request not in list(
            operation.parcel_requests.values_list("parcel_request", flat=True)
        ):
            operation.parcel_requests.create(
                parcel_request=ParcelRequest.objects.get(pk=parcel_request)
            )
            return redirect(reverse_lazy("operation:detail", kwargs={"pk": pk}))
        else:
            return redirect(reverse_lazy("operation:detail", kwargs={"pk": pk}))


def parcel_requests_delete(request, pk):
    """
    Delete a parcel request from the operation.

    Args:
        request (): The HTTP request object.
        pk (): The primary key of the operation.

    Returns:
        A redirect to the operation detail page.
    """
    if request.method == "POST":
        parcel_request = OperationParcelRequest.objects.get(pk=pk)
        parcel_request.delete()
        return redirect(
            reverse_lazy("operation:detail", kwargs={"pk": parcel_request.operation.pk})
        )


def parcel_return_add(request, pk):
    """
    Add parcel returns to the operation.

    Args:
        request (): The HTTP request object.
        pk (): The primary key of the operation.

    Returns:
        A redirect to the operation detail page.
    """
    if request.method == "POST":
        operation = Operation.objects.get(pk=pk)
        data = request.POST
        parcel_return = int(data.get("parcel_return"))
        if parcel_return not in list(
            operation.parcel_returns.values_list("parcel_return", flat=True)
        ):
            operation.parcel_returns.create(parcel_return=parcel_return)
        return redirect(reverse_lazy("operation:detail", kwargs={"pk": pk}))


def parcel_return_delete(request, pk):
    """
    Delete a parcel return from the operation.

    Args:
        request (): The HTTP request object.
        pk (): The primary key of the operation.

    Returns:
        A redirect to the operation detail page.
    """
    if request.method == "POST":
        parcel_return = OperationParcelReturn.objects.get(pk=pk)
        parcel_return.delete()
        return redirect(
            reverse_lazy("operation:detail", kwargs={"pk": parcel_return.operation.pk})
        )


# function to request approve
def request_open(request, pk):
    """
    Request approve for the operation.

    Args:
        request (): The HTTP request object.
        pk (): The primary key of the operation.

    Returns:
        A redirect to the operation detail page.
    """
    if request.method == "POST":
        operation = Operation.objects.get(pk=pk)
        print(operation)
        operation.operation_status = Operation.OperationStatus.WAIT
        operation.approve_status = Operation.ApproveStatus.WAIT_OPEN
        operation.save()
        return redirect(reverse_lazy("operation:detail", kwargs={"pk": pk}))


def approve_open(request, pk):
    """
    Approve the operation.

    Args:
        request (): The HTTP request object.
        pk (): The primary key of the operation.

    Returns:
        A redirect to the operation detail page.
    """
    if request.method == "POST":
        operation = Operation.objects.get(pk=pk)
        operation.operation_status = Operation.OperationStatus.PROGRESS
        operation.approve_status = Operation.ApproveStatus.APPROVE
        operation.save()
        return redirect(reverse_lazy("operation:detail", kwargs={"pk": pk}))


def request_close(request, pk):
    """
    Request approve for the operation.

    Args:
        request (): The HTTP request object.
        pk (): The primary key of the operation.

    Returns:
        A redirect to the operation detail page.
    """
    if request.method == "POST":
        operation = Operation.objects.get(pk=pk)
        # operation.operation_status = Operation.OperationStatus.DONE
        operation.approve_status = Operation.ApproveStatus.WAIT_CLOSE
        operation.save()
        return redirect(reverse_lazy("operation:detail", kwargs={"pk": pk}))


def approve_close(request, pk):
    """
    Approve the operation.

    Args:
        request (): The HTTP request object.
        pk (): The primary key of the operation.

    Returns:
        A redirect to the operation detail page.
    """
    if request.method == "POST":
        operation = Operation.objects.get(pk=pk)
        operation.operation_status = Operation.OperationStatus.DONE
        operation.approve_status = Operation.ApproveStatus.APPROVE
        operation.save()
        return redirect(reverse_lazy("operation:detail", kwargs={"pk": pk}))


def add_inform(request, pk):
    """
    Add inform to the operation.

    Args:
        request (): The HTTP request object.
        pk (): The primary key of the operation.

    Returns:
        A redirect to the operation detail page.
    """
    if request.method == "POST":
        operation = Operation.objects.get(pk=pk)
        data = request.POST
        inform_id = int(data.get("inform"))
        if inform_id not in operation.informs.all().values_list("inform", flat=True):
            inform = Inform.objects.get(pk=inform_id)
            operation.informs.create(inform=inform)
        return redirect(reverse_lazy("operation:detail", kwargs={"pk": pk}))


def delete_inform(request, pk):
    """
    Delete an inform from the operation.

    Args:
        request (): The HTTP request object.
        pk (): The primary key of the inform.

    Returns:
        A redirect to the operation detail page.
    """
    if request.method == "POST":
        inform = OperationInform.objects.get(pk=pk)
        inform.delete()
        return redirect(
            reverse_lazy("operation:detail", kwargs={"pk": inform.operation.pk})
        )


# FIX: set media path save or delete pdf file after render
def operation_to_pdf(request: HttpResponse, pk: int):
    media = settings.MEDIA_ROOT
    operation = get_object_or_404(Operation, pk=pk)
    operation_media = os.path.join(media, str(operation.id))
    if not os.path.exists(operation_media):
        os.makedirs(operation_media)

    context = {
        "operation": operation,
    }
    temp_html = "inform/temp.html"
    with open(temp_html, "w") as f:
        f.write(render_to_string("inform/inform_pdf.html", {"context": context}))
    pdf = generate_pdf(
        data={"context": context}, template_path="inform/inform_pdf.html"
    )
    os.remove(temp_html)

    response = HttpResponse(pdf, content_type="application/pdf")
    # response["Content-Disposition"] = "attachment; filename=inform.pdf"
    return response
