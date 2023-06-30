from django import forms
from ckeditor.fields import RichTextFormField

from repair.forms import widgets

from asset.models import StockItem
from .models import Inform, InformProgress


class InformForm(forms.ModelForm):
    """
    Form for inform

    Attributes: 
        queryset: StockItem.objects.all()
    """
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

    
class ManagerCheckForm(forms.ModelForm):
    """ Form for manager check """
    class Meta:
        model = Inform
        fields = (
            'repair_category',
            'inform_status',
            'assigned_to',
        )
        labels = {
            'repair_category': 'ประเภทการแจ้งซ่อม',
            'inform_status': 'สถานะการแจ้งซ่อม',
            'assigned_to': 'หัวหน้าชุดซ่อม',
        }

        widgets = {
            'repair_category': widgets.Select(
                attrs={'class': 'form-select'}
            ),
            'inform_status': widgets.HiddenInput(),
            'assigned_to': widgets.Select(
                attrs={'class': 'form-select'}
            )
        }


class ProgressForm(forms.ModelForm):
    """ Form for progress """
    class Meta:
        model = InformProgress
        fields = (
            'note',
            'status',
        )
        labels = {
            'note': 'บันทึก',
            'status': 'สถานะ',
        }
        widgets = {
            'note': forms.Textarea(
                attrs={
                    'class': 'form-control',
                }
            ),
            'status': widgets.Select(
                attrs={'class': 'form-select'}
            ),
        }
