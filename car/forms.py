from django import forms
from django.forms import widgets

from car.models import Car, CarBooking

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
            'mission',
            'passenger',
            'controler',
            'approver',
            'driver',
        )
        widgets = {
            'mission':   widgets.Textarea(attrs={'class': 'form-control'}),
            'passenger': widgets.NumberInput(attrs={'class': 'form-control'}),
            'controler': widgets.Select(attrs={'class': 'form-select'}),
            'approver':  widgets.Select(attrs={'class': 'form-select'}),
            'driver':    widgets.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'mission': 'ภารกิจ',
            'passenger': 'จำนวนผู้โดยสาร',
            'controler': 'ผู้ควบคุม',
            'approver': 'ผู้อนุมัติ',
            'driver': 'พลขับ',
        }
