from django import forms
from django.forms import formset_factory
from .models import (
    RequestBill,
    RequestBillDetail,
    RequestItem
)
from asset.models import StockItem
from account.models import Department


class SelectDepartmentForm(forms.ModelForm):
    department = forms.ModelChoiceField(
        queryset=Department.objects.filter(
            name__startswith='คลัง'
        ),
    )

    class Meta:
        model = RequestBill
        fields = ['department']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['department'].widget.attrs['class'] = 'form-select'
        self.fields['department'].widget.attrs['placeholder'] = 'กรุณาเลือกคลังที่ต้องการ'
