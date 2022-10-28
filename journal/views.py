from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
)

from journal.models import Journal, JournalImage, JournalStatus, JournalType
from journal.forms import JournalForm

# Create your views here.


class JournalListView(LoginRequiredMixin, ListView):
    """JournalListView."""

    model = Journal
    template_name = 'journal/journal.html'

    def get_queryset(self):
        qs = Journal.objects.filter(author=self.request.user)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'บันทึกการปฏิบัติงาน'
        return context

class JournalDetailView(LoginRequiredMixin, DetailView):
    """JournalDetailView."""

    model = Journal
    template_name = 'journal/journal_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['images'] = JournalImage.objects.filter(journal=self.get_object())
        return context


class JournalCreateView(LoginRequiredMixin, CreateView):
    template_name = 'journal/journal_form.html'
    # model = Journal
    form_class    = JournalForm
    success_url   = reverse_lazy('journal:list')
    login_url     = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        context = {
            'form': self.form_class,
            'title': 'Create',
            'header': 'ทึกการปฏิบัติงาน',
            'btn_text': 'Save Work'
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)

        if form.is_valid():
            images    = request.FILES.getlist('images')
            form_save = form.save()
            form_id   = get_object_or_404(Journal, pk=form_save.pk)

            if images:
                for image in images:
                    a_image = JournalImage(journal=form_id, images=image)
                    a_image.save()
            else:
                form_save.save()

            return redirect(self.success_url)
        else:
            form = self.form_class()

        context = {
            'form': form,
            'title': 'Create',
            'header':  'บึนทึกการปฏิบัติงาน',
            'btn_text': 'Save Work'
        }
        return render(request, self.template_name, context)

class JournalUpdateView(LoginRequiredMixin, UpdateView):
    login_url     = reverse_lazy('login')
    template_name = 'journal/journal_form.html'
    form_class    = JournalForm
    model         = Journal
    # success_url = reverse_lazy('journal:list')

    def get_success_url(self):
        return reverse_lazy('journal:detail', kwargs={'pk' : self.get_object().pk})

    def get(self, request, *args, **kwargs):
        form   = self.form_class(instance=self.get_object())
        images = JournalImage.objects.filter(journal=self.get_object())

        context = {
            'form':     form,
            'images':   images,
            'title':    'Update',
            'header':   'อัพเดทบันทึกการปฏิบัติงาน',
            'btn_text': 'บันทึก',
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES, instance=self.get_object())
        if form.is_valid():
            images    = request.FILES.getlist('images')
            form_save = form.save()
            form_id   = get_object_or_404(Journal, pk=form_save.pk)

            if images:
                for image in images:
                    a_image = JournalImage.objects.create(journal=form_id, images=image)
                    a_image.save()
            else:
                form_save.save()

            return redirect(self.get_success_url())

        else:
            form = self.form_class(instance=self.get_object())

        return render(request, self.template_name, {'form': form})

class JournalDeleteView(LoginRequiredMixin, DeleteView):
    model         = Journal
    template_name = 'journal/journal_delete.html'
    success_url   = reverse_lazy('journal:list')

    def get_context_data(self, **kwargs):
        context             = super(JournalDeleteView, self).get_context_data(**kwargs)
        context['title']    = 'Delete'
        context['header']   = 'ลบบันทึกการปฏิบัติงาน'
        context['btn_text'] = 'ยืนยันการลบ'
        context['images'] = JournalImage.objects.filter(journal=self.get_object())
        return context

def JournalCategoriesView(request, pk):
    object_list = Journal.objects.filter(category__id__exact=pk)
    description = JournalType.objects.get(pk=pk)
    context     = {
        'object_list': object_list,
        'description': description,
        'btn':        'Back'
    }
    return render(request, 'journal/journal.html', context)

def JournalStatusView(request, pk):
    object_list = Journal.objects.filter(status__id__exact=pk)
    description = JournalStatus.objects.get(pk=pk)
    context     = {
        'object_list': object_list,
        'description': description,
        'btn':         'Back'
    }
    return render(request, 'journal/journal.html', context)
