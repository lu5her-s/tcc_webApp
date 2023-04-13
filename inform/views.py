import datetime
from django.shortcuts import HttpResponse, redirect, render, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    TemplateView,
)

from inform.forms import InformForm

from .models import Inform, InformImage

# Create your views here.

# User sector


class InformHomeView(LoginRequiredMixin, TemplateView):

    """
    home for all user
    get template_name from user.groups
    """
    # template_name = 'inform/home.html'
    TEMPLATE_NAMES = {
        'StaffRepair': 'inform/manager.html',
        'Technical': 'repair/technical.html',
    }

    def get_template_names(self):
        """
        check user groups
        for return template_name

        Returns: str:template_name
            
        """
        for group in self.request.user.groups.all():
            template_name = self.TEMPLATE_NAMES.get(group.name)
            if template_name:
                return template_name
        return 'inform/user_inform.html'

    # def get_template_names(self):
    #
    #     user_groups = self.request.user.groups.values_list('name', flat=True)
    #     if 'StaffRepair' in user_groups:
    #         return 'inform/manager.html'
    #     elif 'Technical' in user_groups:
    #         return 'repair/technical.html'
    #     else:
    #         return 'repair/user_inform.html'

    # def get_template_names(self):
    #     if self.request.user.groups.filter(name="StaffRepair").exists():
    #         return 'inform/manager.html'
    #     elif self.request.user.groups.filter(name="Technical").exists():
    #         return 'repair/technical.html'
    #     else:
    #         return 'repair/user_inform.html'

    def get_context_data(self, **kwargs):
        department = self.request.user.profile.department
        # user section
        inform_department = Inform.objects.filter(
            customer__profile__department=department,
        )

        today_min = datetime.datetime.combine(
            datetime.date.today(),
            datetime.time.min
        )
        today_max = datetime.datetime.combine(
            datetime.date.today(),
            datetime.time.max
        )

        inform_department_done = inform_department.filter(
            repair_status=Inform.RepairStatus.CLOSE
        )
        inform_agent = inform_department.filter(
            repair_category=Inform.RepairCategory.AGENT,
            approve_status=Inform.ApproveStatus.APPROVE
        )
        inform_agent_done = inform_department.filter(
            repair_category=Inform.RepairCategory.AGENT,
            approve_status=Inform.ApproveStatus.APPROVE,
            repair_status=Inform.RepairStatus.CLOSE
        )
        inform_wait = inform_department.filter(
            repair_category=Inform.RepairCategory.WAIT,
            approve_status=Inform.ApproveStatus.APPROVE,
        )
        inform_wait_done = inform_department.filter(
            repair_category=Inform.RepairCategory.WAIT,
            approve_status=Inform.ApproveStatus.APPROVE,
            repair_status=Inform.RepairStatus.CLOSE
        )
        # end user section

        # manager section
        wait_check = Inform.objects.filter(
            inform_status=Inform.InformStatus.INFORM,
        )
        wait_today = Inform.objects.filter(
            inform_status=Inform.InformStatus.INFORM,
            created_at__range=(today_min, today_max)
        )
        wait_approve = Inform.objects.filter(
            inform_status=Inform.InformStatus.WAIT
        )
        wait_approve_today = Inform.objects.filter(
            inform_status=Inform.InformStatus.WAIT,
            created_at__range=(today_min, today_max)
        )

        context = {
            'inform_department': inform_department,
            'inform_department_done': inform_department_done,
            'inform_agent': inform_agent,
            'inform_agent_done': inform_agent_done,
            'inform_wait': inform_wait,
            'inform_wait_done': inform_wait_done,

            # Manager
            'wait_check' : wait_check,
            'wait_today': wait_today,
            'wait_approve': wait_approve,
            'wait_approve_today': wait_approve_today,
        }
        return super().get_context_data(**context)


class InformDetailView(LoginRequiredMixin, DetailView):
    template_name = "inform/inform_detail.html"
    model = Inform
    # queryset = Inform.objects.select_related()


class InformUserListView(LoginRequiredMixin, ListView):
    """ User Inform """
    template_name = 'inform/inform_list.html'
    model = Inform

    def get_queryset(self):
        return super().get_queryset().filter(
            customer=self.request.user
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.request.user.profile
        context['add_inform'] = True
        return context


class InformDepartmentListView(LoginRequiredMixin, ListView):
    """ Department Inform """
    template_name = "inform/inform_list.html"
    model = Inform

    def get_queryset(self):
        return super().get_queryset().filter(
            customer__profile__department=self.request.user.profile.department
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.request.user.profile.department
        context['add_inform'] = True
        return context


class InformAgentListView(LoginRequiredMixin, ListView):
    """ Repair by agent in department """
    template_name = "inform/inform_list.html"
    model = Inform

    def get_queryset(self):
        return super().get_queryset().filter(
            customer__profile__department=self.request.user.profile.department,
            repair_category=Inform.RepairCategory.AGENT,
            approve_status=Inform.ApproveStatus.APPROVE,
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "ที่ต้องดำเนินการ"
        return context


class InformWaitListView(LoginRequiredMixin, ListView):
    """ Wait for job inform """
    template_name = 'inform/inform_list.html'
    model = Inform

    def get_queryset(self):
        return super().get_queryset().filter(
            customer__profile__department=self.request.user.profile.department,
            repair_category=Inform.RepairCategory.WAIT,
            approve_status=Inform.ApproveStatus.APPROVE
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "รอวงรอบการดำเนินการ"
        return context


class InformCreateView(LoginRequiredMixin, CreateView):
    """
    for create new inform_create
    and wait for manager check
    """
    template_name = "inform/inform_create.html"
    model = Inform
    form_class = InformForm

    def get_success_url(self):
        return reverse('inform:user_list')

    def get(self, request, *args, **kwargs):
        context = {
            'form': self.form_class(request)
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request, request.POST, request.FILES)
        if form.is_valid():
            inform = form.save()
            if request.FILES:
                images = request.FILES.getlist('images')
                for img in images:
                    a_img = InformImage.objects.create(
                        inform=inform,
                        images=img
                    )
                    a_img.save()
        return redirect(reverse('inform:user_list'))


# Manager sector


class InformManagerListView(LoginRequiredMixin, ListView):
    '''
    Show Inform list for manager to manager
    '''
    template_name = 'inform/inform_list.html'
    model = Inform

    def get_queryset(self):
        return super().get_queryset().filter(
            inform_status=Inform.InformStatus.INFORM,
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'ยังไม่ได้ตรวจสอบ'
        return context


class InformManagerDetailView(LoginRequiredMixin, DetailView):
    """
    show detail infrom for manager
    """
    template_name = 'inform/inform_manager_detail_view.html'
    model = Inform

    def get_context_data(self, **kwargs):
        """
        **kwargs:
        Returns:
        """
        context = super().get_context_data(**kwargs)
        return context


class InformWaitApproveListView(LoginRequiredMixin, ListView):
    """ 
    List of Inform Status WAIT
    wait for command approve
    """
    template_name = 'inform/inform_list.html'
    model = Inform

    def get_queryset(self):
        return super().get_queryset().filter(
            inform_status=Inform.InformStatus.WAIT
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'รอการอนุมัติ'
        return context
