import datetime
from assign.views import Q
from django.shortcuts import HttpResponse, redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template import context
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)
from asset.models import StockItemImage

from inform.forms import InformForm, InformProgress, ProgressForm, ManagerCheckForm

from .models import Inform, InformImage, InformReject

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
        'Technical': 'inform/technical.html',
        'Command': 'inform/command.html',
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
            deleted=False
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
            deleted=False
        )
        wait_today = Inform.objects.filter(
            inform_status=Inform.InformStatus.INFORM,
            created_at__range=(today_min, today_max)
        )
        wait_approve = Inform.objects.filter(
            Q(inform_status=Inform.InformStatus.WAIT) &
            Q(deleted=False)
        )
        wait_approve_today = Inform.objects.filter(
            inform_status=Inform.InformStatus.WAIT,
            created_at__range=(today_min, today_max)
        )

        # technical dashboard
        wait_accept = Inform.objects.filter(
            assigned_to=self.request.user.profile,
            approve_status=Inform.ApproveStatus.APPROVE,
            accepted=False
        )
        in_progress = Inform.objects.filter(
            assigned_to=self.request.user.profile,
            approve_status=Inform.ApproveStatus.APPROVE,
            accepted=True,
            repair_status=Inform.RepairStatus.REPAIR
        )
        wait_job = Inform.objects.filter(
            assigned_to=self.request.user.profile,
            approve_status=Inform.ApproveStatus.APPROVE,
            accepted=True,
            repair_category=Inform.RepairCategory.WAIT
        )
        close_job = Inform.objects.filter(
            assigned_to=self.request.user.profile,
            approve_status=Inform.ApproveStatus.APPROVE,
            accepted=True,
            repair_status=Inform.RepairStatus.CLOSE
        )
        wait_close = Inform.objects.filter(
            assigned_to=self.request.user.profile,
            approve_status=Inform.ApproveStatus.APPROVE,
            accepted=True,
            repair_status=Inform.RepairStatus.COMPLETE
        )

        # command dashboard
        all_inform = Inform.objects.filter(
            approve_status=Inform.ApproveStatus.APPROVE
        )
        all_done = Inform.objects.filter(
           repair_status=Inform.RepairStatus.CLOSE 
        )
        not_done = Inform.objects.filter(
            Q(approve_status=Inform.ApproveStatus.APPROVE) &
            ~Q(repair_status=Inform.RepairStatus.CLOSE)
        )
        not_accept = Inform.objects.filter(
            approve_status=Inform.ApproveStatus.APPROVE,
            accepted=False
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

            # Technical
            'wait_accept': wait_accept,
            'in_progress': in_progress,
            'wait_job': wait_job,
            'close_job': close_job,
            'wait_close': wait_close,

            # Command
            'all_inform': all_inform,
            'all_done': all_done,
            'not_done': not_done,
            'not_accept': not_accept,
        }
        return super().get_context_data(**context)


class InformDetailView(LoginRequiredMixin, DetailView):
    """ For show detail inform separate by user """
    template_name = "inform/inform_detail.html"
    model = Inform
    # queryset = Inform.objects.select_related()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['manager_check'] = ManagerCheckForm(instance=self.get_object())
        context['form'] = ProgressForm(instance=self.get_object())
        context['note'] = InformProgress.objects.filter(inform=self.get_object())
        if InformReject.objects.filter(inform=self.get_object()):
            context['reason'] = InformReject.objects.get(inform=self.get_object())
        return context

    def post(self, request, *args, **kwargs):
        form = ManagerCheckForm(request.POST, instance=self.get_object())

        if form.is_valid():
            inform = Inform.objects.get(pk=self.get_object().pk)
            # change inform_status to WAIT
            inform.inform_status = Inform.InformStatus.WAIT
            inform.repair_category = form.cleaned_data['repair_category']
            inform.assigned_to = form.cleaned_data['assigned_to']
            print(inform)
            print(form.cleaned_data)
            inform.save()
            # return redirect('inform:detail', pk=self.get_object().pk)
            return redirect(reverse_lazy('inform:detail', kwargs={'pk': self.get_object().pk}))
        return super().post(request, *args, **kwargs)


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
        return redirect(reverse_lazy('inform:user_list'))


class InformUpdateView(LoginRequiredMixin, DetailView):
    """ for update inform_update """
    template_name = "inform/inform_update.html"
    model = Inform

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['manager_check'] = ManagerCheckForm(instance=self.object)
        return context


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
        # context 'approve' return true if self.object.approve_status is APPROVE
        context['approve'] = self.object.inform_status
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


class InformUrgencyListView(LoginRequiredMixin, ListView):
    """ 
    List of Inform Status URGENCY
    """
    template_name = 'inform/inform_list.html'
    model = Inform

    def get_queryset(self):
        return super().get_queryset().filter(
            inform_status=Inform.RepairCategory.URGENCY,
            approve_status=Inform.ApproveStatus.APPROVE
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'รายการซ่อมด่วน'
        return context

class InformWaitAgentListView(LoginRequiredMixin, ListView):
    """
    Wait Agent in place get operation
    """
    template_name = 'inform/inform_list.html'
    model = Inform

    def get_queryset(self):
        return super().get_queryset().filter(
            inform_status=Inform.RepairCategory.AGENT,
            approve_status=Inform.ApproveStatus.APPROVE
        )

    def get_context_data(self, **kwargs):
        """
            **kwargs: 

        Returns:
            
        """
        context = super().get_context_data(**kwargs)
        context['title'] = 'รอดำเนินการโดย จนท.ประจำสถานี'
        return context


class InformWaitJobListView(LoginRequiredMixin, ListView):
    """
    Wait for job assigned schedule
    """
    template_name = 'inform/inform_list.html'
    model = Inform

    def get_queryset(self):
        return super().get_queryset().filter(
            inform_status=Inform.RepairCategory.WAIT,
            approve_status=Inform.ApproveStatus.APPROVE
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'รอวงรอบการดำเนินการ'
        return context


class InformCancelListView(LoginRequiredMixin, ListView):
    """
    Inform recheck or cancel
    """
    template_name = 'inform/inform_list.html'
    model = Inform

    def get_queryset(self):
        return super().get_queryset().filter(
            approve_status=Inform.ApproveStatus.REJECT
        )


# Technical sector
class InformTechnicalListView(LoginRequiredMixin, ListView):
    template_name = 'inform/inform_list.html'
    model = Inform

    def get_queryset(self):
        return super().get_queryset().filter(
            approve_status=Inform.ApproveStatus.APPROVE,
            assigned_to=self.request.user.profile,
            accepted=False
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'รายการแจ้งซ่อม'
        return context


class InformInProgressListView(LoginRequiredMixin, ListView):
    template_name = 'inform/inform_list.html'
    model = Inform

    def get_queryset(self):
        return super().get_queryset().filter(
            repair_status=Inform.RepairStatus.REPAIR,
            assigned_to=self.request.user.profile,
            accepted=True
        )


def accept_inform(request, pk):
    inform = get_object_or_404(Inform, pk=pk)
    inform.accepted = True
    inform.repair_status = Inform.RepairStatus.REPAIR
    inform.save(update_fields=['accepted', 'repair_status'])
    return redirect(reverse_lazy('inform:detail', kwargs={'pk': pk}))


def repair_note(request, pk):
    inform = get_object_or_404(Inform, pk=pk)
    repair_status = request.POST.get('status')
    note = request.POST.get('note')
    repair_note = InformProgress.objects.create(
        inform=inform,
        repair_status=repair_status,
        note=note
    )
    # repair_note.save()
    return redirect(reverse_lazy('inform:detail', kwargs={'pk': pk}))


# Command sector
def inform_approve(request, pk):
    inform = get_object_or_404(Inform, pk=pk)
    inform.approve_status = Inform.ApproveStatus.APPROVE
    inform.inform_status = None
    inform.save(update_fields=['approve_status'])
    return redirect(reverse_lazy('inform:detail', kwargs={'pk': pk}))

def inform_reject(request, pk):
    inform = get_object_or_404(Inform, pk=pk)
    inform.approve_status = Inform.ApproveStatus.REJECT
    inform.save(update_fields=['approve_status'])
    reject = InformReject.objects.create(
        inform=inform,
        reason=request.POST.get('reason')
    )
    return redirect(reverse_lazy('inform:detail', kwargs={'pk': pk}))
