from ckeditor.fields import RichTextFormField
from django import forms
from django.contrib.auth.models import User
from django.forms import widgets

from repair.models import Repair
from asset.models import StockItem
from inform.models import Inform, InformImage


# repair form for save data to model
class RepairForm(forms.ModelForm):
    class Meta:
        model = Repair
        fields = (
            'comment',
            'cost',
        )
        labels = {
            'comment': 'รายละเอียด',
            'cost': 'ค่าใช้จ่าย',
        }
