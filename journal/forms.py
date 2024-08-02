from django import forms
from django.forms import widgets
from ckeditor.fields import RichTextField
# from django.contrib.auth.models import User

from journal.models import Journal


class DateInput(widgets.DateTimeBaseInput):
    input_type = "date"
    format_key = "DATE_INPUT_FORMATS"


class JournalForm(forms.ModelForm):
    images = forms.ImageField(
        widget=widgets.ClearableFileInput(
            attrs={"class": "form-control", "multiple": True}
        ),
        label="ภาพการปฏิบัติงาน",
        required=False,
    )

    class Meta:
        model = Journal
        fields = ("title", "category", "body", "status", "header", "images", "author")
        widgets = {
            "title": widgets.TextInput(attrs={"class": "form-control"}),
            "category": widgets.Select(attrs={"class": "form-select"}),
            # 'body':       widgets.Textarea(attrs={'class' : 'form-control'}),
            "body": widgets.Textarea(attrs={"class": "form-control"}),
            "status": widgets.Select(attrs={"class": "form-select"}),
            "header": widgets.Select(attrs={"class": "form-select"}),
            # 'created_at': DateInput(),
            "author": widgets.HiddenInput(
                attrs={"class": "form-control", "id": "author"}
            ),
        }
        labels = {
            "title": "เรื่อง",
            "category": "ประเภท",
            "body": "รายละเอียด",
            "status": "สถานะ",
            "header": "ผุ้ควบคุม/สั่งการ",
            "created_at": "วันที่ปฏิบัติงาน",
        }
