from django import forms
from django.forms import formset_factory
from account.models import Department
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


class RequestItemForm(forms.ModelForm):
    class Meta:
        model = RequestItem
        fields = (
            'item',
            'quantity',
        )
        widgets = {
            'item': forms.Select(attrs={'class': 'form-select'}),
            'quantity': forms.TextInput(attrs={'class': 'form-control'}),
        }


class CartAddForm(forms.Form):
    quantity = forms.TypedChoiceField()
