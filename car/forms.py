from account.models import Profile
from ckeditor.fields import RichTextFormField
from django import forms
from django.forms import widgets

from car.models import Car, CarBooking, CarFix


class DateInput(widgets.DateTimeBaseInput):
    """DateInput."""

    input_type = "date"
    format_key = "DATE_INPUT_FORMATS"


class CarForm(forms.ModelForm):
    """
    CarForm for create new Car

    Attributes:
        images:
    """

    images = forms.ImageField(
        widget=widgets.ClearableFileInput(
            attrs={
                "class": "form-control",
                "multiple": True,
            }
        ),
        label="ภาพเพิ่มเติม",
        required=False,
    )

    class Meta:
        model = Car
        fields = (
            "car_type",
            "number",
            "manufacturer",
            "capacity",
            "fuel_max",
            "fuel_rate",
            "fuel_now",
            "mile_now",
            "responsible_man",
            "status",
            "car_avatar",
            "images",
        )
        widgets = {
            "car_type": widgets.Select(attrs={"class": "form-select"}),
            "number": widgets.TextInput(attrs={"class": "form-control"}),
            "manufacturer": widgets.TextInput(attrs={"class": "form-control"}),
            "capacity": widgets.NumberInput(attrs={"class": "form-control"}),
            "fuel_max": widgets.NumberInput(attrs={"class": "form-control"}),
            "fuel_rate": widgets.NumberInput(attrs={"class": "form-control"}),
            "fuel_now": widgets.NumberInput(attrs={"class": "form-control"}),
            "mile_now": widgets.NumberInput(attrs={"class": "form-control"}),
            "responsible_man": widgets.Select(attrs={"class": "form-select"}),
            "status": widgets.Select(attrs={"class": "form-select"}),
            "car_avatar": widgets.ClearableFileInput(attrs={"class": "form-control"}),
        }
        labels = {
            "car_type": "ประเภท",
            "number": "หมายเลขทะเบียน",
            "manufacturer": "ยี่ห้อ/รุ่น",
            "capacity": "จำนวนผู้โดยสาร",
            "fuel_max": "อัตราเชื้อเพลิงเต็มถัง",
            "fuel_rate": "อัตราการใช้เชื้อเพลิง(กม./ลิตร)",
            "fuel_now": "ปริมาณเชื้อเพลิง",
            "mile_now": "เลขไมล์ปัจจุบัน",
            "responsible_man": "ผู้รับผิดชอบ",
            "status": "สถานะ",
            "car_avatar": "ภาพยานพาหนะ",
        }


class BookingForm(forms.ModelForm):
    """
    BookingForm for create new CarBooking
    """

    class Meta:
        model = CarBooking
        fields = (
            "car",
            "mission",
            "passenger",
            "controler",
            "approver",
            "driver",
            "requested_at",
            "status",
            "requester",
        )
        widgets = {
            "car": widgets.HiddenInput(attrs={"class": "form-control"}),
            "mission": widgets.Textarea(attrs={"class": "form-control", "rows": 3}),
            "passenger": widgets.NumberInput(attrs={"class": "form-control"}),
            "controler": widgets.Select(attrs={"class": "form-select"}),
            "approver": widgets.Select(attrs={"class": "form-select"}),
            "driver": widgets.Select(attrs={"class": "form-select"}),
            "status": widgets.Select(attrs={"class": "form-select"}),
            "requested_at": widgets.DateTimeInput(
                attrs={
                    "class": "form-control",
                    "type": "datetime-local",
                    "id": "datepicker",
                },
                # format='yyyy-MM-ddThh:mm'
            ),
            "requester": widgets.HiddenInput(attrs={"class": "form-control"}),
        }
        labels = {
            "mission": "ภารกิจ",
            "passenger": "จำนวนผู้โดยสาร",
            "controler": "ผู้ควบคุม",
            "approver": "ผู้อนุมัติ",
            "driver": "พลขับ",
            "requested_at": "วันที่ใช้งาน",
            "status": "สถานะ",
        }


class ApproveForm(forms.ModelForm):
    car_ref = forms.CharField(
        widget=widgets.HiddenInput(
            attrs={
                "class": "form-control",
            }
        ),
        label="สถานะการขอใช้",
    )

    class Meta:
        model = CarBooking
        fields = ("status",)
        widgets = {
            "status": widgets.Select(attrs={"class": "form-select"}),
        }
        labels = {
            "status": "สถานะการขอใช้",
        }


class CarReturnForm(forms.Form):
    """
    CarReturnForm for return mile

    Attributes:
        mile_current:
    """

    mile_current = forms.FloatField(
        label="เลขไมล์ปัจจุบัน",
        required=False,
        min_value=0,
        widget=forms.NumberInput(
            attrs={"class": "form-control", "placeholder": "เลขไมล์ปัจจุบัน", "step": "0.1"}
        ),
    )


class CarRefuelForm(forms.Form):
    """
    CarRefuelForm for refuel

    Attributes:
        mile_refuel:
        note:
        refuel:
    """

    mile_refuel = forms.FloatField(
        label="ไมล์เติมน้ำมัน",
        required=False,
        min_value=0,
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "placeholder": "ไมล์เติมน้ำมัน",
                "step": "0.1",
            }
        ),
    )
    note = forms.CharField(
        label="บันทึก",
        required=False,
        widget=forms.Textarea(attrs={"class": "form-control"}),
    )
    refuel = forms.FloatField(
        label="จำนวนน้ำมันที่เติม",
        required=True,
        min_value=1.0,
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "placeholder": "จำนวนน้ำมันที่เติม (ลิตร)",
                "step": "0.1",
            }
        ),
    )


class CarRequestFixForm(forms.ModelForm):
    """
    CarRequestFixForm for request fix

    Attributes:
        images:
    """

    images = forms.ImageField(
        label="รูปภาพ",
        required=False,
        widget=forms.ClearableFileInput(
            attrs={
                "class": "form-control",
                "multiple": True,
            }
        ),
    )

    class Meta:
        model = CarFix
        fields = [
            "car",
            "issue",
            "fix_requester",
            "approver",
            # 'requested_at',
            "approve_status",
            "responsible_man",
            # 'note',
            "images",
        ]
        widgets = {
            "car": forms.HiddenInput(attrs={"class": "form-control"}),
            "issue": RichTextFormField(),
            "fix_requester": forms.HiddenInput(attrs={"class": "form-control"}),
            "approver": forms.Select(attrs={"class": "form-select"}),
            "finished_at": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "datetime-local",
                }
            ),
            "approve_status": forms.Select(attrs={"class": "form-select"}),
            "responsible_man": forms.Select(attrs={"class": "form-select"}),
        }
        help_texts = {
            "images": "อัพโหลดรูปภาพที่เกี่ยวข้องกับการซ่อมบำรุง",
        }
        labels = {
            "issue": "อาการ/สารเหตุ",
            "approver": "ผู้อนุมัติ",
            "approve_status": "สถานะการอนุมัติ",
            "responsible_man": "มอบหมายผู้ดำเนินการ",
        }

        # def init fields approver is profile__use group is Car
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields["approver"].queryset = Profile.objects.filter(
                user__groups__name="Car"
            )


class CarAfterFixForm(forms.ModelForm):
    """
    CarAfterFixForm for after fix

    Attributes:
        fixed_image:
    """

    fixed_image = forms.ImageField(
        label="รูปภาพการซ่อม",
        required=False,
        widget=forms.FileInput(
            attrs={
                "class": "form-control",
                "multiple": True,
            }
        ),
    )

    class Meta:
        model = CarFix
        fields = [
            "fix_status",
            "note",
            "cost_use",
            "fixed_image",
        ]
        labels = {
            "fix_status": "สถานะการซ่อม",
            "note": "บันทึกการซ่อมบำรุง",
            "cost_use": "ค่าใช้จ่าย",
            "fixed_image": "รูปภาพการซ่อม",
        }
        widgets = {
            "fix_status": forms.Select(attrs={"class": "form-select"}),
            "note": RichTextFormField(),
            "cost_use": forms.NumberInput(
                attrs={"class": "form-control", "min_value": 0}
            ),
        }


class ApproverForm(forms.ModelForm):
    class Meta:
        model = CarFix
        fields = {
            "fix_status",
            "responsible_man",
        }
        widgets = {
            "fix_status": forms.Select(attrs={"class": "form-select"}),
            "responsible_man": forms.Select(attrs={"class": "form-select"}),
        }
        labels = {
            "fix_status": "สถานะการอนุมัติ",
            "responsible_man": "มอบหมายผู้ดำเนินการ",
        }
