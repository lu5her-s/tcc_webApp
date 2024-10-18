from django import forms
from django.contrib.auth.models import User
from django.forms import formset_factory, widgets
from car.models import CarBooking
from . import models


class OperationForm(forms.ModelForm):
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


class TaskForm(forms.ModelForm):
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
    car_booking = forms.ModelChoiceField(
        queryset=CarBooking.objects.filter(approve_status__name="อนุมัติ"),
        label="การจองรถ",
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["car_booking"].label_from_instance = lambda obj: obj


class AddFuelForm(forms.Form):
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
