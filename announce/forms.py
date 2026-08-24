from django import forms
from django.forms import widgets

from .models import Announce


class MultipleFileInput(widgets.ClearableFileInput):
    allow_multiple_selected = True


class AnnounceForm(forms.ModelForm):
    """
    ModelForm for Announce creation

    Attributes:
        files:
        images:
    """

    files = forms.FileField(
        widget=MultipleFileInput(attrs={"class": "form-control"}),
        label="เอกสารที่เกี่ยวข้อง",
        required=False,
    )
    images = forms.ImageField(
        widget=MultipleFileInput(attrs={"class": "form-control"}),
        label="รูปภาพ",
        required=False,
    )

    class Meta:
        model = Announce
        fields = (
            "is_type",
            "title",
            "detail",
            "status",
            "author",
            "images",
            "files",
        )
        widgets = {
            "is_type": widgets.Select(attrs={"class": "form-select"}),
            "title": widgets.TextInput(attrs={"class": "form-control"}),
            "detail": widgets.Textarea(attrs={"class": "form-control"}),
            # 'detail' : CKEditorWidget(attrs={'class': 'w3-input'}),
            "status": widgets.Select(attrs={"class": "form-select"}),
            "author": widgets.HiddenInput(
                attrs={"class": "form-control", "id": "author"}
            ),
        }
        labels = {
            "is_type": "ประเภท",
            "title": "ชื่อเรื่อง",
            "detail": "รายละเอียด",
            "status": "สถานะ",
            "author": "ผู้เขียน",
        }


class SearchForm(forms.Form):
    text = forms.CharField(label="Search", required=False)
