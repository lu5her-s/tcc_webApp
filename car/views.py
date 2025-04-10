#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : views.py
# Author            : lu5her <lu5her@mail>
# Date              : Wed Nov, 23 2022, 19:31 327
# Last Modified Date: Sun Mar, 09 2025, 12:34 068
# Last Modified By  : lu5her <lu5her@mail>
import datetime
from itertools import chain

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import (
    HttpResponseRedirect,
    get_object_or_404,
    redirect,
    render,
)
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from car.forms import (
    ApproveForm,
    BookingForm,
    CarAfterFixForm,
    CarForm,
    CarRefuelForm,
    CarRequestFixForm,
    CarReturnForm,
)
from car.models import (
    Car,
    CarAfterFixImage,
    CarBooking,
    CarFix,
    CarFixImage,
    CarImage,
    Refuel,
)

# Create your views here.


class CarListView(LoginRequiredMixin, ListView):
    """
    CarListView for Car app

    Attributes:
        model:
        template_name:
    """

    model = Car
    template_name = "car/car.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "รายการยานพาหนะ"
        return context


class CarCreateView(LoginRequiredMixin, CreateView):
    """
    for create new Car

    Attributes:
        model:
        form_class:
        template_name:
        success_url:
    """

    model = Car
    form_class = CarForm
    template_name = "car/create.html"
    success_url = reverse_lazy("car:list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Create"
        context["form"] = self.form_class
        context["header"] = "เพิ่มยานพาหนะ"
        return context

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)

        if form.is_valid():
            images = request.FILES.getlist("images")
            form_save = form.save()
            form_id = get_object_or_404(Car, pk=form_save.pk)

            if images:
                for image in images:
                    a_image = CarImage(car=form_id, images=image)
                    a_image.save()
            else:
                form_save.save()

            return redirect(self.success_url)
        else:
            form = self.form_class()
        return super().post(request, *args, **kwargs)


class CarUpdateView(LoginRequiredMixin, UpdateView):
    """
    for update Car

    Attributes:
        template_name:
        form_class:
        model:
    """

    template_name = "car/create.html"
    form_class = CarForm
    model = Car
    # success_url = reverse_lazy('car:detail', kwargs={'pk': self.get_object().pk})

    def get_success_url(self):
        return reverse_lazy("car:detail", kwargs={"pk": self.get_object().pk})


class CarDetailView(LoginRequiredMixin, DetailView):
    """
    DetailView for Car

    Attributes:
        template_name:
        model:
        object:
    """

    template_name = "car/detail.html"
    model = Car

    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        context = super().get_context_data(**kwargs)
        context["car_use"] = CarBooking.objects.filter(car=self.object)
        context["refuel"] = Refuel.objects.filter(car=self.object)
        context["car_fix"] = CarFix.objects.filter(car=self.object)
        try:
            context["booking_list"] = Car.objects.get(
                pk=self.object.pk
            ).car_booking.all()
            context["booking"] = Car.objects.get(pk=self.object.pk).car_booking.get()
        except:
            context["booking_list"] = None
            context["booking"] = None
        return context


# DONE: make booking list views
class CarBookingListView(LoginRequiredMixin, ListView):
    """
    CarBookingListView for CarBooking app
    list all booking

    Attributes:
        template_name:
        model:
    """

    template_name = "car/booking.html"
    model = CarBooking

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "รายการขอใช้ยานพาหนะ"
        return context

    def get_queryset(self):
        if self.request.user.groups.filter(
            name="Car"
        ).exists() or self.request.user.groups.filter(name="Staff"):
            qs = CarBooking.objects.all()

        else:
            qs = CarBooking.objects.filter(
                Q(requester=self.request.user)
                | Q(driver=self.request.user.profile)
                | Q(approver=self.request.user.profile)
            )
        return qs


# DONE: make booking create view
class CarBookingCreateView(LoginRequiredMixin, CreateView):
    """
    CarBookingCreateView for create new CarBooking

    Attributes:
        template_name:
        model:
        form_class:
        success_url:
    """

    template_name = "car/booking_form.html"
    model = CarBooking
    form_class = BookingForm
    success_url = reverse_lazy("car:booking")

    def get(self, *args, **kwargs):
        context = {
            "form": self.form_class,
            "car_ref": kwargs["pk"],
            "car": Car.objects.get(pk=kwargs["pk"]),
        }
        return render(self.request, self.template_name, context)

    def post(self, request, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form_save = form.save()
            car = Car.objects.get(pk=kwargs["pk"])
            car.status = Car.Status.PENDING
            car.save()
            return redirect(self.success_url)
        else:
            print(form.errors)
            form = self.form_class()
        context = {
            "from": form,
            "car_ref": kwargs["pk"],
        }
        return render(request, self.template_name, context)


class CarBookingDetailView(LoginRequiredMixin, DetailView):
    """
    CarBookingDetailView for CarBooking app

    Attributes:
        model:
        template_name:
    """

    model = CarBooking
    template_name = "car/booking_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


def update_approve(request, pk):
    """
    update_approve for update approve status
    """
    # booking = CarBooking.objects.get(pk=pk)
    form = ApproveForm()
    if request.method == "POST":
        form = ApproveForm(request.POST)
        if form.is_valid():
            form.save()
            return reverse_lazy("car:booking-detail", kwargs={"pk": pk})
    else:
        form = ApproveForm()
    context = {
        "form": form,
    }
    return render(request, "car/car.html", context)


class CarBookingUpdateView(LoginRequiredMixin, UpdateView):
    """
    Update CarBooking

    Attributes:
        template_name:
        model:
        form_class:
        object:
        object:
    """

    template_name = "car/booking_form.html"
    model = CarBooking
    form_class = BookingForm

    def get_success_url(self):
        self.object = self.get_object()
        return reverse("car:booking-detail", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        context = super().get_context_data(**kwargs)
        context["form"] = self.form_class(instance=self.object)
        context["car_ref"] = self.object.car.pk
        context["test_var"] = self.object.car.number

        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, instance=self.get_object())
        if form.is_valid():
            form.save()
            # a_status = ApproveStatus.objects.get(pk=request.POST.get('approve_status'))
            if request.POST["approve_status"] == "APPROVE":
                car = Car.objects.get(pk=request.POST.get("car"))
                print(car)
                car.status = Car.Status.WAIT
                car.save()
            return redirect(self.get_success_url())
        else:
            form = self.form_class(instance=self.get_object())
        context = {"form": self.form_class(instance=self.get_object())}
        return render(request, self.template_name, context)


def car_booking_approve(request, pk):
    """
    car_booking_approve for approve booking

    Args:
        request ():
        pk ():

    Returns:

    """
    if request.method == "POST":
        booking = CarBooking.objects.get(pk=pk)
        # booking.approver = request.user.profile
        booking.status = CarBooking.Status.APPROVE
        booking.save()
        return redirect(reverse_lazy("car:booking-detail", kwargs={"pk": pk}))


def car_booking_reject(request, pk):
    """
    car_booking_reject for reject booking

    Args:
        request ():
        pk ():

    Returns:

    """
    if request.method == "POST":
        booking = CarBooking.objects.get(pk=pk)
        # booking.approver = request.user.profile
        booking.approve = CarBooking.Status.REJECT
        booking.save()
        return redirect(reverse_lazy("car:booking-detail", kwargs={"pk": pk}))


class WaitApproveListView(LoginRequiredMixin, ListView):
    """
    WaitApproveListView for CarBooking app

    Attributes:
        template_name:
        model:
    """

    template_name = "car/wait_approve.html"
    model = CarBooking

    def get_queryset(self):
        qs = CarBooking.objects.filter(status=CarBooking.Status.PENDING)
        return qs


def ReturnCar(request, pk):
    """
    ReturnCar for return mile

    Args:
        request ():
        pk ():

    Returns:

    """
    form = CarReturnForm()
    booking = CarBooking.objects.get(pk=pk)
    car = Car.objects.get(pk=booking.car.pk)
    # booking.mile_out = car.mile_now

    distance: float = 0
    fuel_use: float = 0
    if request.method == "POST":
        form = CarReturnForm(request.POST)
        if form.is_valid():
            distance: float = round(
                (float(request.POST.get("mile_current")) - car.mile_now), 2
            )
            fuel_use: float = distance / car.fuel_rate
            booking.mile_out = car.mile_now
            booking.distance = distance
            booking.mile_in = request.POST["mile_current"]
            booking.return_at = datetime.datetime.now()
            booking.fuel_use = fuel_use
            booking.status = CarBooking.Status.DONE
            car.mile_now = request.POST["mile_current"]
            car.fuel_now = car.fuel_now - fuel_use
            car.status = Car.Status.READY
            booking.save()
            car.save()
            return redirect(reverse_lazy("car:booking"))
        # print(request.POST['mile_current'])
    else:
        form = CarReturnForm()
    context = {
        "form": form,
        "car": car,
        "distance": distance,
        "fuel_use": fuel_use,
        "mile_now": car.mile_now + distance,
        "fuel_now": car.fuel_now - fuel_use,
        "booking": booking,
    }
    return render(request, "car/return.html", context)


# DONE: add mile_out in this
def UseCar(request, pk):
    """
    UseCar for use car

    Args:
        request ():
        pk ():

    Returns:

    """
    car = Car.objects.get(pk=pk)
    car.status = Car.Status.INUSE
    car.save()
    return HttpResponseRedirect(reverse("car:booking"))


def RefuelCar(request, pk):
    """
    RefuelCar for refuel car

    Args:
        request ():
        pk ():

    Returns:

    """
    car = Car.objects.get(pk=pk)
    form = CarRefuelForm()
    if request.method == "POST":
        form = CarRefuelForm(request.POST)
        if form.is_valid():
            fuel_old = car.fuel_now
            re_fuel = float(request.POST["refuel"])
            fuel_new = fuel_old + re_fuel
            if fuel_new <= car.fuel_max:
                fuel_new = fuel_new
            else:
                fuel_new = car.fuel_max
            print("Mile :", request.POST["mile_refuel"])
            print("refuel :", request.POST["refuel"])
            print("New Fuel : ", fuel_new)
            print(request.POST["note"])
            refuel_db = Refuel.objects.create(
                car=car,
                refuel=re_fuel,
                mile_refuel=request.POST["mile_refuel"],
                refueler=request.user,
                note=request.POST["note"],
            )
            refuel_db.save()
            car.fuel_now = fuel_new
            car.save()
            return redirect("car:detail", pk=car.id)
    context = {
        "car": car,
        "form": form,
    }
    return render(request, "car/refuel.html", context)


class CarFixCreateView(LoginRequiredMixin, CreateView):
    """
    CarFixCreateView for create new CarFix

    Attributes:
        model:
        template_name:
    """

    model = CarFix
    template_name = "car/fix_form.html"
    # form_class = CarRequestFixForm

    def post(self, request, **kwargs):
        # get POST data
        car_pk = kwargs["pk"]
        car = Car.objects.get(pk=car_pk)
        form = CarRequestFixForm(request.POST, request.FILES)
        if form.is_valid():
            car.status = Car.Status.FIX
            car.save()
            fix_db = form.save()
            # save images
            images = request.FILES.getlist("images")
            for image in images:
                fix_img = CarFixImage(fix=fix_db, images=image)
                fix_img.save()
            # redirect to car detail page
            return redirect("car:fix-detail", pk=fix_db.pk)
        # else:
        # print(form.errors)
        context = {
            "car": car,
            "form": form,
        }
        return render(request, self.template_name, context)

    def get(self, request, **kwargs):
        # return car and form
        car_pk = kwargs["pk"]
        car = Car.objects.get(pk=car_pk)
        form = CarRequestFixForm()
        # form.fields['approver'] = Profile.objects.filter(user__is_staff=True)
        context = {
            "car": car,
            "form": form,
        }
        return render(request, self.template_name, context)


class CarRequestFixListView(LoginRequiredMixin, ListView):
    """
    CarRequestFixListView for CarFix app

    Attributes:
        template_name:
        model:
    """

    template_name = "car/request_fix.html"
    model = CarFix

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "รายการแจ้งซ่อม"
        return context


class CarRequestFixDetailView(LoginRequiredMixin, DetailView):
    """
    CarRequestFixDetailView for CarFix app

    Attributes:
        template_name:
        model:
        object:
    """

    template_name = "car/fix_detail.html"
    model = CarFix

    # get_context_data images
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.object = self.get_object()
        qs1 = CarFixImage.objects.filter(fix=self.object)
        qs2 = CarAfterFixImage.objects.filter(fix=self.object)
        context["all_imgs"] = list(chain(qs1, qs2))
        context["fix_image"] = CarAfterFixImage.objects.filter(fix=self.object)
        context["images"] = CarFixImage.objects.filter(fix=self.object)
        return context


def CarAfterFixView(request, pk):
    """
    CarAfterFixView for CarFix app

    Args:
        request ():
        pk ():

    Returns:

    """
    fix = CarFix.objects.get(pk=pk)
    car = Car.objects.get(pk=fix.car.pk)
    form = CarAfterFixForm(instance=fix)
    if request.method == "POST":
        form = CarAfterFixForm(request.POST, request.FILES)
        if form.is_valid():
            fix.note = request.POST["note"]
            fix.cost_use = request.POST["cost_use"]
            fix.fix_status = CarFix.Status.FINISHED
            # fix finished_at now()
            fix.finished_at = datetime.datetime.now()
            # approve_status change to name = "เสร็จสิ้น"
            fix.approve_status = CarFix.ApproveStatus.DONE
            # save image to CarAfterFixImage
            for f in request.FILES.getlist("fixed_image"):
                CarAfterFixImage.objects.create(fix=fix, images=f)
            # save fix
            fix.save()
            return redirect("car:fix-detail", pk=fix.pk)
    context = {
        "form": form,
        "fix": fix,
        "car": car,
    }
    return render(request, "car/afterfix_form.html", context)


class CarFixUpdateView(LoginRequiredMixin, UpdateView):
    """
    CarFixUpdateView for update CarFix

    Attributes:
        model:
        form_class:
        template_name:
        object:
    """

    model = CarFix
    form_class = CarRequestFixForm
    template_name = "car/fix_form.html"
    # success_url = reverse_lazy('car:fix')

    # def post
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            fix = form.save()
            # fix_id = get_object_or_404(CarFix, pk=fix.pk)
            # save image
            if request.FILES.getlist("images"):
                for f in request.FILES.getlist("images"):
                    CarFixImage.objects.create(fix=fix, images=f)
                # save fix
            fix.save()
            return redirect("car:fix-detail", pk=fix.pk)
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        fix = CarFix.objects.get(pk=self.kwargs["pk"])
        car = Car.objects.get(pk=fix.car.pk)
        images = CarFixImage.objects.filter(fix=fix)
        context = super().get_context_data(**kwargs)
        context["title"] = "แก้ไขการซ่อม"
        # context['fix'] = fix
        context["car"] = car
        context["images"] = images
        # context['form'] = CarRequestFixForm(instance=self.get_object())
        # context['app_form'] = ApproverForm(instance=self.get_object())
        return context


class CarFixDeleteView(LoginRequiredMixin, DeleteView):
    """
    CarFixDeleteView for delete CarFix

    Attributes:
        model:
        template_name:
        success_url:
    """

    model = CarFix
    template_name = "car/fix_confirm_delete.html"
    success_url = reverse_lazy("car:fix")


class ResponsibleListView(LoginRequiredMixin, ListView):
    """
    ResponsibleListView for CarFix app

    Attributes:
        template_name:
        model:
    """

    template_name = "car/fix_list.html"
    model = CarFix

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "รายการซ่อมที่รับผิดชอบ"
        return context

    def get_queryset(self):
        return CarFix.objects.filter(responsible_man=self.request.user.profile)
