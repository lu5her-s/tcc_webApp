import datetime
from django.shortcuts import (
    redirect,
    render,
    reverse,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    TemplateView,
    ListView,
    DetailView,
)

from .models import Inform, InformImage
from .forms import InformForm

# Create your views here.
# TODO: make manager


class RepairHome(LoginRequiredMixin, TemplateView):
    """
    RepairHome.
    Show Home page of Repair app
    separate template with user group
    Staff and RepairStaff => manager.html
    Technical => technical.html
    User or Member => user_inform.html
    context = [
        inform status = INF
    ]
    """

    # template_name = 'repair/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['inform'] = Inform.objects.filter(
            status=Inform.RepairStatus.INFORM
        )
        today_min = datetime.datetime.combine(
            datetime.date.today(),
            datetime.time.min
        )
        today_max = datetime.datetime.combine(
            datetime.date.today(),
            datetime.time.max
        )
        context['today_inf'] = Inform.objects.filter(
            created_at__range=(today_min, today_max)
        )

        context['user_operator'] = Inform.objects.filter(
            assigned_to=self.request.user.profile,
            approve=Inform.ApproveStatus.APPROVE
        )
        # user dashboard
        context['user_inform'] = Inform.objects.filter(
            customer=self.request.user
        )
        context['user_today_inform'] = Inform.objects.filter(
                customer=self.request.user,
                approve=Inform.ApproveStatus.APPROVE,
                created_at__range=(today_min, today_max),
        )
        context['user_job_inform'] = Inform.objects.filter(
            customer__profile__department=self.request.user.profile.department,
            status=Inform.RepairStatus.WAIT,
            approve=Inform.ApproveStatus.APPROVE
        )
        return context

    def get_template_names(self):
        if self.request.user.groups.filter(name="StaffRepair").exists():
            return 'repair/manager.html'
        elif self.request.user.groups.filter(name="Technical").exists():
            return 'repair/technical.html'
        else:
            return 'repair/user_inform.html'


class InformListView(LoginRequiredMixin, ListView):
    """
    InformListView.
    show only inform status == inform
    """

    template_name = 'repair/inform.html'
    model = Inform

    def get_queryset(self):
        return super().get_queryset().filter(status=Inform.RepairStatus.INFORM)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'ยังไม่ได้ตรวจสอบ'
        context['add_inform'] = True
        return context


class InformDetailView(LoginRequiredMixin, DetailView):
    template_name = 'repair/inform_detail.html'
    model = Inform

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "การแจ้งซ่อม"
        context['images'] = InformImage.objects.filter(
            inform=self.get_object()
        )
        return context


class InformCreateView(LoginRequiredMixin, CreateView):
    template_name = 'repair/inform_form.html'
    form_class = InformForm
    model = Inform

    def get(self, request, *args, **kwargs):
        form = self.form_class(request)
        context = {
            'form': form,
        }
        return render(self.request, self.template_name, context)

    def post(self, request, **kwargs):
        form = self.form_class(request, request.POST, request.FILES)
        if form.is_valid():
            # print(form.cleaned_data)
            inform = form.save()
            if request.FILES:
                images = request.FILES.getlist('images')
                for img in images:
                    a_img = InformImage.objects.create(
                        inform=inform,
                        images=img
                    )
                    a_img.save()
            return redirect(reverse_lazy('repair:inform'))
        else:
            print(form.errors)
            return render(request, self.template_name, {'form': form})


class InformDepartmentListView(LoginRequiredMixin, ListView):
    template_name = 'repair/inform.html'

    def get_queryset(self):
        qs = Inform.objects.filter(
            stockitem__location=self.request.user.profile.department
        )
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.request.user.profile.department
        context['add_inform'] = True
        return context


class InformAssignedListView(LoginRequiredMixin, ListView):
    template_name = 'repair/inform.html'

    def get_queryset(self):
        qs = Inform.objects.filter(
            assigned_to=self.request.user.profile
        )
        return qs


class InformJobDepartmentListView(LoginRequiredMixin, ListView):
    template_name = 'repair/inform.html'

    def get_queryset(self):
        qs = []
        if self.request.user.groups.filter(name="StaffRepair").exists():
            qs = Inform.objects.filter(
                status=Inform.RepairStatus.WAIT,
                approve=Inform.ApproveStatus.APPROVE
            )
        elif self.request.user.groups.filter(name="Technical").exists():
            qs = Inform.objects.filter(
                assigned_to=self.request.user.profile,
                status=Inform.RepairStatus.WAIT,
                approve=Inform.ApproveStatus.APPROVE
            )
        else:
            qs = Inform.objects.filter(
                customer__profile__department=self.request.user.profile.department,
                status=Inform.RepairStatus.WAIT,
                approve=Inform.ApproveStatus.APPROVE
            )

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'รอวงรอบการซ่อมบำรุง'
        return context