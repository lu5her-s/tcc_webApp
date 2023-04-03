from django import forms
from ckeditor.fields import RichTextFormField

from repair.forms import widgets

from asset.models import StockItem
from .models import Inform


class InformForm(forms.ModelForm):
    images = forms.ImageField(
        widget=widgets.ClearableFileInput(
            attrs={
                'class': 'form-control',
                'multiple': True
            }
        ),
        label='ภาพประกอบการแจ้งซ่อม',
        required=False
    )

    class Meta:
        model = Inform
        fields = (
            'urgency',
            'stockitem',
            'issue_category',
            'issue',
            'customer',
        )
        widgets = {
            'stockitem': widgets.Select(
                attrs={'class': 'form-select'}
            ),
            'issue_category': widgets.Select(
                attrs={'class': 'form-select'}
            ),
            'issue': RichTextFormField(),
            'urgency': widgets.Select(
                attrs={'class': 'form-select'}
            ),
        }
        labels = {
            'urgency': 'ความเร่งด่วน',
            'stockitem': 'พัสดุที่แจ้งซ่อม',
            'issue_category': 'ประเภทการแจ้งซ่อม',
            'issue': 'อาการ/สาเหตุ',
            'customer': 'ผู้แจ้ง',
        }

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # field stockitem query only in user.profile.department
        self.fields['stockitem'].queryset = StockItem.objects.filter(
            location=request.user.profile.department
        )
