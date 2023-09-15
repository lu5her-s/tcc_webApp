#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : views.py
# Author            : lu5her <lu5her@mail>
# Date              : Thu Sep, 14 2023, 15:33 257
# Last Modified Date: Thu Sep, 14 2023, 16:13 257
# Last Modified By  : lu5her <lu5her@mail>
import datetime
import re
from django.db.models import Q
from django.shortcuts import HttpResponse, redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from account.models import LineToken
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    TemplateView,
)
from config.sendline import Sendline

from inform.forms import InformForm, InformProgress, ProgressForm, ManagerCheckForm, ReviewForm
from repair.forms import Repair

from .models import (
    CommandReview,
    CustomerReview,
    Inform,
    InformImage,
    InformReject,
    ManagerReview
)

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
        customer_review = CustomerReview.objects.filter(
            reviewer=self.request.user
        )
        inform_wait_review = Inform.objects.filter(
            Q(approve_status=Inform.ApproveStatus.APPROVE) &
            Q(repair_status=Inform.RepairStatus.CLOSE) &
            ~Q(closed=True)
        )
        inform_wait_to_review = inform_wait_review.exclude(
            customer_review__in=customer_review
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
            Q(approve_status=None) &
            Q(deleted=False)
        )
        wait_approve_today = Inform.objects.filter(
            inform_status=Inform.InformStatus.WAIT,
            created_at__range=(today_min, today_max)
        )
        urgency_wait = Inform.objects.filter(
            inform_status=Inform.InformStatus.WAIT,
            repair_category=Inform.RepairCategory.URGENCY
        )
        urgency_done = Inform.objects.filter(
            repair_status=Inform.RepairStatus.CLOSE,
            repair_category=Inform.RepairCategory.URGENCY
        )
        agent_wait = Inform.objects.filter(
            inform_status=Inform.InformStatus.WAIT,
            repair_category=Inform.RepairCategory.AGENT
        )
        agent_done = Inform.objects.filter(
            repair_status=Inform.RepairStatus.CLOSE,
            repair_category=Inform.RepairCategory.AGENT
        )
        job_wait = Inform.objects.filter(
            repair_category=Inform.RepairCategory.WAIT,
            approve_status=Inform.ApproveStatus.APPROVE
        )
        job_done = Inform.objects.filter(
            repair_status=Inform.RepairStatus.CLOSE,
            repair_category=Inform.RepairCategory.WAIT
        )
        recheck = Inform.objects.filter(
            approve_status=Inform.ApproveStatus.REJECT
        )
        wait_close = Inform.objects.filter(
            approve_status=Inform.ApproveStatus.APPROVE,
            accepted=True,
            repair_status=Inform.RepairStatus.CLOSE
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

        # command dashboard
        all_inform = Inform.objects.all()
        approve = Inform.objects.filter(
            approve_status=Inform.ApproveStatus.APPROVE,
            deleted=False
        )
        wait_approve = Inform.objects.filter(
            inform_status=Inform.InformStatus.WAIT,
            approve_status=None
        )
        all_done = Inform.objects.filter(
           repair_status=Inform.RepairStatus.CLOSE 
        )
        not_done = Inform.objects.filter(
            Q(approve_status=Inform.ApproveStatus.APPROVE) &
            ~Q(repair_status=Inform.RepairStatus.CLOSE) &
            Q(accepted=True)
        )
        not_accept = Inform.objects.filter(
            Q(approve_status=Inform.ApproveStatus.APPROVE) &
            ~Q(repair_status=Inform.RepairStatus.CLOSE) &
            Q(accepted=False)
        )
        reject = Inform.objects.filter(
            approve_status=Inform.ApproveStatus.REJECT
        )
        wait_close_approve = Inform.objects.filter(
            approve_status=Inform.ApproveStatus.APPROVE,
            repair_status=Inform.RepairStatus.CLOSE,
            closed=False
        )

        context = {
            'inform_department': inform_department,
            'inform_department_done': inform_department_done,
            'inform_agent': inform_agent,
            'inform_agent_done': inform_agent_done,
            'inform_wait': inform_wait,
            'inform_wait_done': inform_wait_done,
            'inform_wait_to_review': inform_wait_to_review,

            # Manager
            'wait_check' : wait_check,
            'wait_today': wait_today,
            'wait_approve': wait_approve,
            'wait_approve_today': wait_approve_today,
            'urgency_wait': urgency_wait,
            'urgency_done': urgency_done,
            'agent_wait': agent_wait,
            'agent_done': agent_done,
            'job_wait': job_wait,
            'job_done': job_done,
            'recheck': recheck,

            # Technical
            'wait_accept': wait_accept,
            'in_progress': in_progress,
            'wait_job': wait_job,
            'close_job': close_job,
            'wait_close': wait_close,

            # Command
            'all_inform': all_inform,
            'approve': approve,
            'all_done': all_done,
            'not_done': not_done,
            'not_accept': not_accept,
            'reject': reject,
            'wait_close_approve': wait_close_approve
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
        context['images'] = InformImage.objects.filter(inform=self.get_object())
        context['approve'] = self.get_object().approve_status
        context['repairs'] = Repair.objects.filter(inform=self.get_object())
        context['review_form'] = ReviewForm()
        
        try:
            context['customer_review'] = CustomerReview.objects.get(inform=self.get_object())
            context['manager_review'] = ManagerReview.objects.get(inform=self.get_object())
            context['command_review'] = CommandReview.objects.get(inform=self.get_object())
        except:
            pass

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
            if inform.repair_category == Inform.RepairCategory.AGENT:
                inform.assigned_to = inform.customer.profile
            inform.save()
            token = LineToken.objects.get(name="Manager").token
            line = Sendline(token)
            body = 'มีการแจ้งซ่อมรออนุมัติ'
            body += f'\nหมายเลขการแจ้งซ่อม: {inform.pk}'
            body += f'\nประเภทงาน: {inform.get_repair_category_display()}'
            url = request.build_absolute_uri(reverse_lazy('inform:detail', kwargs={'pk': inform.pk}))
            body += f'\nurl : {url}'
            line.sendtext(body)
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
        pk = self.get_object().pk
        return reverse_lazy('inform:detail', kwargs={'pk': pk})

    def get(self, request, *args, **kwargs):
        context = {
            'form': self.form_class(request)
        }
        return render(request, self.template_name, context)

    def remove_html(self, text):
        return re.sub('<[^<]+?>', '', text)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request, request.POST, request.FILES)
        if form.is_valid():
            inform = form.save()
            token = LineToken.objects.get(name='Manager').token
            images = request.FILES.getlist('images') if 'images' in request.FILES else None
            if images:
                InformImage.objects.bulk_create(
                    [
                        InformImage(inform=inform, images=image) for image in images
                    ]
                )
            # host = request.get_host()
            # path = reverse_lazy('inform:detail', kwargs={'pk': inform.pk})
            # url  = 'http://' + host + path
            url = request.build_absolute_uri(reverse_lazy('inform:detail', kwargs={'pk': inform.pk}))
            issue_clear = self.remove_html(form.cleaned_data['issue'])
            # body = ''
            body = '\nมีแจ้งซ่อมใหม่: '
            body += f'\nหมายเลขใบแจ้งซ่อม : {inform.pk}/{inform.created_at.year+543}'
            body += f'\nวันที่แจ้งซ่อม : {inform.created_at.strftime("%d/%m/%Y")}'
            body += f'\nความเร่งด่วน : {inform.get_urgency_display()}'
            body += f'\nสถานที่ : {inform.customer.profile.department}'
            body += f'\nผู้แจ้งซ่อม : {inform.customer.profile if inform.customer.profile else inform.customer}'
            body += f'\nอุปกรณ์ที่แจ้งซ่อม : {inform.stockitem.item_name}'
            body += f'\nอาการ : \n{issue_clear}'
            body += f'\n\nurl : {url}'

            line  = Sendline(token)
            try:
                line.sendtext(body)
            except Exception as e:
                print(e)
        return redirect(reverse_lazy('inform:home'))


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


def staff_wait_close(request):
    inform = Inform.objects.filter(
        repair_status=Inform.RepairStatus.CLOSE
    )
    return render(request, 'inform/inform_list.html', {'object_list': inform})


def accept_inform(request, pk):
    inform = get_object_or_404(Inform, pk=pk)
    inform.accepted = True
    inform.repair_status = Inform.RepairStatus.REPAIR
    inform.save(update_fields=['accepted', 'repair_status'])
    InformProgress.objects.create(
        inform=inform,
        status=Inform.RepairStatus.ACCEPT,
        note="ตอบรับการดำเนินการแล้ว"
    )
    return redirect(reverse_lazy('inform:detail', kwargs={'pk': pk}))


def repair_note(request, pk):
    inform = get_object_or_404(Inform, pk=pk)

    if request.method == 'POST':
        repair_status = request.POST.get('status')
        note = request.POST.get('note')

        repair_note = InformProgress.objects.create(
            inform=inform,
            status=repair_status,
            note=note
        )
        inform.repair_status = repair_status
        inform.save(update_fields=['repair_status'])

        return redirect(reverse_lazy('inform:detail', kwargs={'pk': pk}))


# Command sector
def inform_approve(request, pk):
    inform = get_object_or_404(Inform, pk=pk)
    inform.approve_status = Inform.ApproveStatus.APPROVE
    inform.inform_status = None
    inform.save(update_fields=['approve_status'])
    token = LineToken.objects.get(name="Manager").token
    line = Sendline(token)
    body = f'อนุมัติแจ้งซ่อม : {inform.pk}/{inform.created_at.year+543}'
    line.sendtext(body)
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


# def review_save(request, pk):
#     inform = get_object_or_404(Inform, pk=pk)
#     if request.method == 'POST':
#         if request.user.group.name == 'Manager':
#             ManagerReview.objects.create(
#                 inform=inform,
#                 description=request.POST.get('description'),
#                 rating=request.POST.get('rating'),
#                 reviewer=request.user
#             )
#         elif request.user.group.name == 'Command':
#             CommandReview.objects.create(
#                 inform=inform,
#                 description=request.POST.get('description'),
#                 rating=request.POST.get('rating'),
#                 reviewer=request.user
#             )
#         else:
#             CustomerReview.objects.create(
#                 inform=inform,
#                 description=request.POST.get('description'),
#                 rating=request.POST.get('rating'),
#                 reviewer=request.user
#             )
#         return redirect(reverse_lazy('inform:detail', kwargs={'pk': pk}))
#     else:
#         return redirect(reverse_lazy('inform:detail', kwargs={'pk': pk}))


def review_save(request: HttpResponse, pk: int):
    inform = get_object_or_404(Inform, pk=pk)

    if request.method == 'POST':
        description = request.POST.get('description')
        rating = request.POST.get('rating')
        reviewer = request.user
        user_group_name = reviewer.groups.values_list('name', flat=True)
        print(user_group_name)


        review_data = {
            'inform': inform,
            'description': description,
            'rating': rating,
            'reviewer': reviewer,
        }
        if "StaffRepair" in user_group_name:
            ManagerReview.objects.create(**review_data)
        elif 'Command' in user_group_name:
            CommandReview.objects.create(**review_data)
            inform.closed = True
            inform.save(update_fields=['closed'])
        else:
            CustomerReview.objects.create(**review_data)
        
        # review_model.objects.create(**review_data)

    return redirect(reverse_lazy('inform:detail', kwargs={'pk': pk}))


def customer_wait_to_review(request: HttpResponse):
    inform = Inform.objects.filter(
        approve_status=Inform.ApproveStatus.APPROVE,
        repair_status=Inform.RepairStatus.CLOSE,
    )
    customer_review = CustomerReview.objects.filter(reviewer=request.user)
    inform_wait_to_review = inform.exclude(customer_review__in=customer_review)

    return render(request, 'inform/inform_list.html', {'object_list': inform_wait_to_review})


def wait_close_approve(request: HttpResponse):
    object_list = Inform.objects.filter(
        Q(repair_status=Inform.RepairStatus.CLOSE) &
        Q(approve_status=Inform.ApproveStatus.APPROVE) &
        Q(closed=False)
    )
    return render(request, 'inform/inform_list.html', {'object_list': object_list, 'title': 'ขออนุมัติปิดงาน'})


def command_wait_approve(request: HttpResponse):
    object_list = Inform.objects.filter(
        inform_status=Inform.InformStatus.WAIT,
        approve_status=None
    )
    return render(request, 'inform/inform_list.html', {'object_list': object_list, 'title': 'รายการรอการอนุมัติ'})


def all_inform(request: HttpResponse):
    object_list = Inform.objects.all()
    return render(request, 'inform/inform_list.html', {'object_list': object_list, 'title': 'รายการทั้งหมด'})


def all_progress(request: HttpResponse):
    object_list = Inform.objects.filter(repair_status=Inform.RepairStatus.REPAIR)
    return render(request, 'inform/inform_list.html', {'object_list': object_list, 'title': 'รายการกำลังดําเนินการ'})


def all_recheck(request: HttpResponse):
    object_list = Inform.objects.filter(approve_status=Inform.ApproveStatus.REJECT)
    return render(request, 'inform/inform_list.html', {'object_list': object_list, 'title': 'รายการตรวจสอบอีกครั้ง'})


def close_approve(request: HttpResponse, pk: int):
    if request.method == 'POST':
        inform = get_object_or_404(Inform, pk=pk)
        inform.closed = True
        inform.save(update_fields=['closed'])
        return redirect(reverse_lazy('inform:detail', kwargs={'pk': pk}))
