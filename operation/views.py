#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : views.py
# Author            : lu5her <lu5her@mail>
# Date              : Sun Jun, 30 2024, 16:53 182
# Last Modified Date: Wed Aug, 14 2024, 12:42 227
# Last Modified By  : lu5her <lu5her@mail>
# -----
from django.db.models import Sum
from django.views.generic import DetailView, ListView, TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect, render

from account.models import Department
from car.forms import CarReturnForm
from car.models import CarBooking

from .models import (
    AllowanceWithdraw,
    OilReimburesment,
    Operation,
    OperationCar,
    Task,
    Team,
    TeamMember,
    Allowance,
)
from .forms import (
    CarAddForm,
    OperationForm,
    TaskForm,
    TaskNoteForm,
    TeamForm,
    TeamMemberFormSet,
    AddFuelForm,
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
        context["user_opreation_wait_close"] = user_all_operation.filter(
            operation_status="WC"
        )
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
            # for note form
            "note_form": TaskNoteForm,
            # for allowance
            "allowances": AllowanceWithdraw.objects.filter(
                allowance__operation=self.object
            ),
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


def accept_leader(request, pk):
    """
    Leader Accept Operation

    Args:
        request ():
        pk ():

    Returns:

    """
    team = Team.objects.get(pk=pk)
    team.accept()
    team.save()
    return redirect(reverse_lazy("operation:detail", kwargs={"pk": team.operation.pk}))


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
        OperationCar.objects.create(
            operation=operation,
            car_booking=CarBooking.objects.get(pk=data.get("car_booking")),
        )
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
