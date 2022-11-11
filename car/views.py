from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
)
from car.forms import BookingForm, CarForm

from car.models import (
    Car,
    CarFix,
    CarImage,
    CarBooking,
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
        return context


# TODO : make booking views
class CarBookingView(LoginRequiredMixin, CreateView):

    """Docstring for CarBookingView. """

    model = CarBooking
    template_name = 'car/booking.html'
    form_class = BookingForm

    def get(self, request, pk):
        car = get_object_or_404(Car, pk=pk)
        # form = self.form_class(kwargs={'car_id': car.id})
        context = {
            'form': self.form_class,
            'title': 'Booking',
            'header': 'จองยานพาหนะ',
            'test_pk': pk,
        }
        return render(request, self.template_name, context)
