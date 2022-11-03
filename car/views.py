from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import (
    CreateView,
    ListView,
)
from car.forms import CarForm

from car.models import (
    Car,
    CarImage,
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
