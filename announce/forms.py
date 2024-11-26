from account.models import LineToken
from ckeditor.widgets import CKEditorWidget
from django import forms
from django.forms import widgets

from .models import Announce, Comment


class LineTokenMultiple(forms.ModelMultipleChoiceField):
    def label_form_instance(self, obj: LineToken) -> str:
        return obj.name


class AnnounceForm(forms.ModelForm):
    """
    ModelForm for Announce creation

    Attributes:
        files:
        images:
        tokens:
    """

    files = forms.FileField(
        widget=forms.ClearableFileInput(
            attrs={"class": "form-control", "multiple": True}
        ),
        label="เอกสารที่เกี่ยวข้อง",
        required=False,
    )
    images = forms.ImageField(
        widget=forms.ClearableFileInput(
            attrs={"class": "form-control", "multiple": True}
        ),
        label="รูปภาพ",
        required=False,
    )
    tokens = LineTokenMultiple(
        queryset=LineToken.objects.all(),
        label="การแจ้งเตือน",
        widget=widgets.CheckboxSelectMultiple(),
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
            "tokens",
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
            "tokens": "การแจ้งเตือน",
        }


class SearchForm(forms.Form):
    text = forms.CharField(label="Search", required=False)
