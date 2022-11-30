#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : views.py
# Author            : lu5her <lu5her@mail>
# Date              : Wed Nov, 23 2022, 19:31 327
# Last Modified Date: Thu Dec, 01 2022, 00:49 335
# Last Modified By  : lu5her <lu5her@mail>
from django.shortcuts import (
    HttpResponse,
    get_object_or_404,
    redirect,
    render
)
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
    View,
)
from car.forms import ApproveForm, BookingForm, CarForm, CarReturnForm

from car.models import (
    ApproveStatus,
    Car,
    CarFix,
    CarImage,
    CarBooking,
    CarStatus,
    Refuel,
)

# Create your views here.

class CarListView(LoginRequiredMixin, ListView):
    model = Car
    template_name = 'car/car.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'รายการยานพาหนะ'
        return context


class CarCreateView(LoginRequiredMixin, CreateView):
    model = Car
    form_class = CarForm
    template_name = 'car/create.html'
    success_url = reverse_lazy('car:list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create'
        context['form'] = self.form_class
        context['header'] = 'เพิ่มยานพาหนะ'
        return context

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)

        if form.is_valid():
            images = request.FILES.getlist('images')
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


class CarDetailView(LoginRequiredMixin, DetailView):
    template_name = 'car/detail.html'
    model = Car

    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        context = super().get_context_data(**kwargs)
        context['car_use'] = CarBooking.objects.filter(car=self.object)
        context['refuel'] = Refuel.objects.filter(car=self.object)
        context['car_fix'] = CarFix.objects.filter(car=self.object)
        try:
            context['booking_list'] = Car.objects.get(pk=self.object.pk).car_booking.all()
            context['booking'] = Car.objects.get(pk=self.object.pk).car_booking.get()
            # context['fix_list'] = CarFix.objects.filter(car=self.object.pk).car.pk
            # context['fixing'] = CarFix.objects.get(car=self.object.pk)
            # context['fix_list'] = Car.objects.get(pk=self.object.pk).car_fix.get().car.pk
            # context['car_fix'] = Car.objects.get(pk=self.object.pk).car_fix.get()
        except:
            context['booking_list'] = None
            context['booking'] = None
            # context['fix_list'] = None
            # context['fixing'] = None
        return context


# DONE: make booking list views
class CarBookingListView(LoginRequiredMixin, ListView):

    """Docstring for CarBookingListView. """
    template_name = 'car/booking.html'
    model = CarBooking

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'รายการขอใช้ยานพาหนะ'
        context['form'] = ApproveForm()
        return context


# TODO: make booking create view
class CarBookingCreateView(LoginRequiredMixin, CreateView):
    template_name = 'car/booking_form.html'
    model = CarBooking
    form_class = BookingForm
    success_url = reverse_lazy('car:booking')

    def get(self, *args, **kwargs):
        context = {
            'form' : self.form_class,
            'car_ref': kwargs['pk'],
        }
        return render(self.request, self.template_name, context)

    def post(self, request, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form_save = form.save()
            car = Car.objects.get(pk=kwargs['pk'])
            car.status = CarStatus.objects.get(name="จอง")
            car.save()
            return redirect(self.success_url)
        else:
            print(form.errors)
            form = self.form_class()
        context = {
            'from': form,
            'car_ref': kwargs['pk'],
        }
        return render(request, self.template_name, context)


class CarBookingDetailView(LoginRequiredMixin, DetailView):
    model = CarBooking
    template_name = 'car/booking_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

def update_approve(request, pk):
    """TODO: Docstring for update_approve.
    :returns: TODO

    """
    # booking = CarBooking.objects.get(pk=pk)
    form = ApproveForm()
    if request.method == 'POST':
        form = ApproveForm(request.POST)
        if form.is_valid():
            form.save()
            return reverse_lazy('car:booking-detail', kwargs={'pk': pk})
    else:
        form = ApproveForm()
    context = {
        'form': form,
    }
    return render(request, 'car/car.html', context)


class CarBookingUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'car/booking_form.html'
    model = CarBooking
    form_class = BookingForm

    def get_success_url(self):
        self.object = self.get_object()
        return reverse('car:booking-detail', kwargs = {'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class(instance=self.object)
        context['car_ref'] = self.object.car.pk
        context['test_var'] = self.object.car.number

        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, instance=self.get_object())
        if form.is_valid():
            form.save()
            return redirect(self.get_success_url())
        else:
            form = self.form_class(instance=self.object)
        context = {
            'form': self.form_class(instance=self.get_object())
        }
        return render(request, self.template_name, context)


class WaitApproveListView(LoginRequiredMixin, ListView):
    template_name = 'car/wait_approve.html'
    model = CarBooking

    def get_queryset(self):
        qs = CarBooking.objects.filter(approve_status__name='รออนุมัติ')
        return qs

def ReturnCar(request, pk):
    form = CarReturnForm()
    car = Car.objects.get(pk=pk)
    distance: int = 0
    fuel_use: float = 0
    if request.method == 'POST':
        form = CarReturnForm(request.POST)
        distance = int(request.POST.get('mile_current')) - car.mile_now
        fuel_use = distance / car.fuel_rate
    else:
        form = CarReturnForm()
    context = {
        'form': form,
        'car': car,
        'distance': distance,
        'fuel_use': fuel_use,
    }
    return render(request, 'car/return.html', context)
