from django import forms
from django.forms import widgets

from car.models import Car, CarBooking


class DateInput(widgets.DateTimeBaseInput):
    """DateInput."""

    input_type = 'date'
    format_key = 'DATE_INPUT_FORMATS'


class CarForm(forms.ModelForm):
    images = forms.ImageField(
        widget = widgets.ClearableFileInput(
            attrs={
                'class': 'form-control',
                'multiple': True,
            }
        ),
        label = 'ภาพเพิ่มเติม',
        required = False
    )

    class Meta:
        model   = Car
        fields  = ('type', 'number', 'manufacturer', 'capacity', 'fuel_max', 'fuel_rate', 'fuel_now', 'mile_now', 'responsible_man', 'status', 'car_avatar', 'images',)
        widgets = {
            'type':            widgets.Select(attrs={'class':             'form-select'}),
            'number':          widgets.TextInput(attrs={'class':        'form-control'}),
            'manufacturer':    widgets.TextInput(attrs={'class':          'form-control'}),
            'capacity':        widgets.NumberInput(attrs={'class':        'form-control'}),
            'fuel_max':        widgets.NumberInput(attrs={'class':        'form-control'}),
            'fuel_rate':       widgets.NumberInput(attrs={'class':        'form-control'}),
            'fuel_now':        widgets.NumberInput(attrs={'class':        'form-control'}),
            'mile_now':        widgets.NumberInput(attrs={'class':        'form-control'}),
            'responsible_man': widgets.Select(attrs={'class':             'form-select'}),
            'status':          widgets.Select(attrs={'class':             'form-select'}),
            'car_avatar':      widgets.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        labels ={
            'type':            'ประเภท',
            'number':          'หมายเลขทะเบียน',
            'manufacturer':    'ยี่ห้อ/รุ่น',
            'capacity':        'จำนวนผู้โดยสาร',
            'fuel_max':        'อัตราเชื้อเพลิงเต็มถัง',
            'fuel_rate':       'อัตราการใช้เชื้อเพลิง(กม./ลิตร)',
            'fuel_now':        'ปริมาณเชื้อเพลิง',
            'mile_now':        'เลขไมล์ปัจจุบัน',
            'responsible_man': 'ผู้รับผิดชอบ',
            'status':          'สถานะ',
            'car_avatar':      'ภาพยานพาหนะ',
        }


class BookingForm(forms.ModelForm):
    class Meta:
        model = CarBooking
        fields = (
            'car',
            'mission',
            'passenger',
            'controler',
            'approver',
            'driver',
            'requested_at',
            'approve_status',
            'requester',
        )
        widgets = {
            'car': widgets.HiddenInput(attrs={'class': 'form-control'}),
            'mission':   widgets.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'passenger': widgets.NumberInput(attrs={'class': 'form-control'}),
            'controler': widgets.Select(attrs={'class': 'form-select'}),
            'approver':  widgets.Select(attrs={'class': 'form-select'}),
            'driver':    widgets.Select(attrs={'class': 'form-select'}),
            'approve_status': widgets.Select(attrs={'class': 'form-select'}),
            'requested_at': widgets.DateTimeInput(
                attrs={'class': 'form-control',
                       'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'
            ),
            'requester': widgets.HiddenInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'mission': 'ภารกิจ',
            'passenger': 'จำนวนผู้โดยสาร',
            'controler': 'ผู้ควบคุม',
            'approver': 'ผู้อนุมัติ',
            'driver': 'พลขับ',
            'requested_at': 'วันที่ใช้งาน',
            'approve_status': 'สถานะ',
        }


class ApproveForm(forms.ModelForm):
    car_ref = forms.CharField(
        widget=widgets.HiddenInput(attrs={
            'class': 'form-control',
        }),
        label="สถานะการขอใช้"
    )
    class Meta:
        model = CarBooking
        fields = (
            'approve_status',
        )
        widgets = {
            'approve_status': widgets.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'approve_status': 'สถานะการขอใช้',
        }


class CarReturnForm(forms.Form):
    mile_current = forms.IntegerField(
        label="Current Miles",
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'miles now'})
    )
