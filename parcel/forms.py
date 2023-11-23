from django import forms
from django.forms import formset_factory
from account.models import Department, Profile
from .models import (
    RequestBill,
    RequestBillDetail,
    RequestItem
)


class SelectStockForm(forms.Form):
    department = forms.ModelChoiceField(queryset=None, required=True)

    class Meta:
        fields = ('department',)
        labels = {
            'department': 'เลือกคลัง'
        }
        widgets = {
            'department': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['department'].queryset = Department.objects.filter(name__startswith='คลัง')


# class BillCreateForm(forms.ModelForm):
#     class Meta:
#         model = RequestBill
#         fields = (
#             'receiver',
#         )
#         widgets = {
#             'receiver': forms.Select(attrs={'class': 'form-select'}),
#         }


class RequestBillDetailForm(forms.ModelForm):
    class Meta:
        model = RequestBillDetail
        fields = (
            'request_case',
            'item_type',
            'item_control',
            'money_type',
            'job_no',
            'receiver'
        )
        widgets = {
            'request_case': forms.Select(attrs={'class': 'form-select'}),
            'item_type': forms.Select(attrs={'class': 'form-select'}),
            'item_control': forms.Select(attrs={'class': 'form-select'}),
            'money_type': forms.Select(attrs={'class': 'form-select'}),
            'job_no': forms.TextInput(attrs={'class': 'form-control'}),
            'receiver': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['request_case'].queryset = RequestBillDetail.RequestCase
        self.fields['receiver'].queryset = Profile.objects.all()
