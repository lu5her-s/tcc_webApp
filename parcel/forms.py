from django import forms
from account.models import Department, Profile
from .models import (
    ParcelReturnDetail,
    RequestBillDetail,
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
            'request_reference',
            'receiver',
            'bill',
        )
        widgets = {
            'request_case': forms.Select(attrs={'class': 'form-select'}),
            'item_type': forms.TextInput(attrs={'class': 'form-control'}),
            'item_control': forms.TextInput(attrs={'class': 'form-control'}),
            'money_type': forms.TextInput(attrs={'class': 'form-control'}),
            'job_no': forms.TextInput(attrs={'class': 'form-control'}),
            'request_reference': forms.TextInput(attrs={'class': 'form-control'}),
            'receiver': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'request_case': 'เบิกในกรณี',
            'item_type': 'ประเภท สป.',
            'item_control': 'สายงานควบคุม',
            'money_type': 'ประเภทเงิน',
            'job_no': 'เลขที่งาน',
            'request_reference': 'เอกสารอ้างอิง',
            'receiver': 'ผู้รับแทน',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['request_case'].queryset = RequestBillDetail.RequestCase
        self.fields['receiver'].queryset = Profile.objects.all()


class ReturnBillDetailForm(forms.ModelForm):
    class Meta:
        model = ParcelReturnDetail
        fields = (
            'return_case',
            'item_type',
            'item_control',
            'money_type',
            'job_no',
            'return_no',
        )
        widgets = {
            'return_case': forms.Select(attrs={'class': 'form-select'}),
            'item_type': forms.TextInput(attrs={'class': 'form-control'}),
            'item_control': forms.TextInput(attrs={'class': 'form-control'}),
            'money_type': forms.TextInput(attrs={'class': 'form-control'}),
            'job_no': forms.TextInput(attrs={'class': 'form-control'}),
            'return_no': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'return_case': 'เหตุที่ส่งคืน',
            'item_type': 'ประเภท สป.',
            'item_control': 'สายงานควบคุม',
            'money_type': 'ประเภทเงิน',
            'job_no': 'เลขที่งาน',
            'return_no': 'ทะเบียนหน่วยรับคืน',
        }

