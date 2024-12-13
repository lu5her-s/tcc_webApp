from car.models import CarBooking
from django import forms
from django.contrib.auth.models import User
from django.db.models import Q
from django.forms import formset_factory, widgets
from inform.models import Inform

from operation.models import ParcelRequest, ParcelReturn

from . import models


class OperationForm(forms.ModelForm):
    """
    OperationForm for create new Operation
    """

    class Meta:
        model = models.Operation
        fields = (
            "type_of_work",
            "start_date",
            "end_date",
            "description",
        )
        widgets = {
            "type_of_work": widgets.Select(attrs={"class": "form-select"}),
            "start_date": widgets.DateInput(
                format=["%d %b %Y"],
                attrs={
                    "class": "form-control",
                    "type": "date",
                },
            ),
            "end_date": widgets.DateInput(
                format=("%d-%b-%Y"),
                attrs={"class": "form-control", "type": "date"},
            ),
            "description": widgets.Textarea(
                attrs={"class": "form-control", "rows": "3"}
            ),
        }
        labels = {
            "type_of_work": "ประเภทงาน",
            "start_date": "วันที่เริ่มงาน",
            "end_date": "วันที่สิ้นสุดงาน",
            "description": "รายละเอียดงาน",
        }

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields["inform"] = forms.ModelChoiceField(
    #         queryset=Inform.objects.filter(approve_status="APR"),
    #         widget=forms.Select(attrs={"class": "form-select"}),
    #         label="อ้างถึงแจ้งซ่อม",
    #     )


class TaskForm(forms.ModelForm):
    """
    TaskForm for create new Task
    """

    class Meta:
        model = models.Task
        fields = (
            "workplace",
            "priority",
            "task",
        )
        widgets = {
            "workplace": widgets.Select(attrs={"class": "form-select"}),
            "priority": widgets.Select(attrs={"class": "form-select"}),
            "task": widgets.Textarea(attrs={"class": "form-control", "rows": "3"}),
        }
        labels = {
            "workplace": "สถานที่ปฏิบัติงาน",
            "priority": "ความสําคัญ",
            "task": "รายละเอียดงาน",
        }


class TeamForm(forms.ModelForm):
    """
    TeamForm for create new Team

    Attributes:
        queryset:
        label_from_instance:
    """

    class Meta:
        model = models.Team
        fields = ("team_leader",)
        widgets = {"team_leader": widgets.Select(attrs={"class": "form-select"})}
        labels = {"team_leader": "หัวหน้าชุด"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["team_leader"].queryset = User.objects.filter(profile__isnull=False)
        self.fields["team_leader"].label_from_instance = lambda obj: obj.profile


# class TeamMemberForm(forms.ModelForm):
#     class Meta:
#         model = models.TeamMember
#         fields = ["member"]
#         widgets = {"member": widgets.Select(attrs={"class": "form-select"})}
#         labels = {"member": "สมาชิก"}
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields["member"].queryset = User.objects.filter(
#             profile__isnull=False
#         ).exclude(team_leader__isnull=False)
#         self.fields["member"].label_from_instance = lambda obj: obj.profile
class TeamMemberForm(forms.Form):
    """
    TeamMemberForm for create new TeamMember

    Attributes:
        member:
        label_from_instance:
    """

    member = forms.ModelChoiceField(
        queryset=User.objects.filter(
            profile__isnull=False, profile__department__name="ส่วนกลาง"
        ),
        label="ลูกชุด",
        widget=forms.Select(
            attrs={"class": "form-select member-select", "required": False}
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["member"].label_from_instance = lambda obj: obj.profile


TeamMemberFormSet = formset_factory(TeamMemberForm, extra=1, can_delete=True)


# FIX: approve_status__name after fix in car.models
class CarAddForm(forms.Form):
    """
    CarAddForm for create new CarAdd

    Attributes:
        car_booking:
        label_from_instance:
    """

    car_booking = forms.ModelChoiceField(
        queryset=CarBooking.objects.filter(status="APPROVE"),
        label="การจองรถ",
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["car_booking"].label_from_instance = lambda obj: obj


class AddFuelForm(forms.Form):
    """
    AddFuelForm for create new AddFuel

    Attributes:
        diesel:
        benzine:
    """

    diesel = forms.FloatField(
        min_value=0.0,
        max_value=9999.9,
        label="ดีเซล",
        widget=forms.NumberInput(attrs={"class": "form-control"}),
        initial=0.0,
    )
    benzine = forms.FloatField(
        min_value=0.0,
        max_value=9999.9,
        label="เบนซิน",
        widget=forms.NumberInput(attrs={"class": "form-control"}),
        initial=0.0,
    )


class TaskNoteForm(forms.Form):
    """
    TaskNoteForm for create new TaskNote

    Attributes:
        status:
        note:
        choices:
    """

    status = forms.ChoiceField(
        label="สถานะ",
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    note = forms.CharField(
        widget=forms.Textarea(attrs={"class": "form-control", "rows": "3"}),
        label="บันทึก",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["status"].choices = models.Task.Status.choices


class OperationParcelRequestForm(forms.Form):
    """
    OperationParcelRequestForm for create new OperationParcelRequest

    Attributes:
        parcel_request:
    """

    parcel_request = forms.ModelChoiceField(
        queryset=ParcelRequest.objects.filter(billdetail__approve_status="APPROVED"),
        label="ใบเบิก",
        widget=forms.Select(attrs={"class": "form-select"}),
    )


class OperationParcelReturnForm(forms.Form):
    """
    OperationParcelReturnForm for create new OperationParcelReturn

    Attributes:
        parcel_return:
    """

    parcel_return = forms.ModelChoiceField(
        queryset=ParcelReturn.objects.filter(billdetail__approve_status="APPROVED"),
        label="ใบส่งคืน",
        widget=forms.Select(attrs={"class": "form-select"}),
    )


class AddInformForm(forms.Form):
    """
    AddInformForm for create new AddInform

    Attributes:
        inform:
    """

    inform = forms.ModelChoiceField(
        queryset=Inform.objects.filter(
            Q(approve_status="APR") & ~Q(repair_status="CLO")
        ),
        label="อ้างถึงแจ้งซ่อม",
        widget=forms.Select(attrs={"class": "form-select"}),
    )
