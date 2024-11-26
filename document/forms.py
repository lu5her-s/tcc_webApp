#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : forms.py
# Author            : lu5her <lu5her@mail>
# Date              : Tue Oct, 18 2022, 16:49 291
# Last Modified Date: Tue Nov, 01 2022, 15:00 305
# Last Modified By  : lu5her <lu5her@mail>
from django import forms
from django.forms import widgets

from account.models import Profile, Sector
from document.models import Document, Depart, Operator


class DateInput(widgets.DateTimeBaseInput):
    """DateInput."""

    input_type = "date"
    format_key = "DATE_INPUT_FORMATS"


class DocumentForm(forms.ModelForm):
    """DocumentForm.
    for create document or recieve document
    """

    #     assigned_sector = forms.ModelMultipleChoiceField(
    # queryset = Sector.objects.all(),
    # widget   = widgets.CheckboxSelectMultiple(attrs={
    # 'class': 'form-checkbox-inline',
    # 'multiple': True,
    # }),
    # label    = 'สำเนาให้แผนก',
    # )

    class Meta:
        model = Document
        fields = (
            "recieve_number",
            "doc_sector",
            "urgency",
            "doc_number",
            "title",
            "doc_date",
            "detail",
            "report_to",
            "operation",
            "file",
            "assigned_sector",
        )
        widgets = {
            "recieve_number": widgets.TextInput(attrs={"class": "form-control"}),
            "doc_sector": widgets.TextInput(attrs={"class": "form-control"}),
            "urgency": widgets.Select(attrs={"class": "form-select"}),
            "doc_number": widgets.TextInput(attrs={"class": "form-control"}),
            "title": widgets.Textarea(attrs={"class": "form-control", "rows": "1"}),
            # 'doc_date':        DateInput(),
            "doc_date": widgets.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "detail": widgets.Textarea(attrs={"class": "form-control"}),
            "report_to": widgets.TextInput(attrs={"class": "form-control"}),
            "operation": widgets.Select(attrs={"class": "form-select"}),
            "file": widgets.ClearableFileInput(attrs={"class": "form-control"}),
            # 'assigned_sector': widgets.CheckboxSelectMultiple(attrs={'class': 'form-check-inline'}),
            "assigned_sector": widgets.SelectMultiple(attrs={"class": "select"}),
            # 'status':        widgets.HiddenInput(attrs={'class':        'form-control', 'id':  'status'}),
        }

        labels = {
            "recieve_number": "เลขรับที่",
            "doc_sector": "หน่วยเจ้าของเรื่อง",
            "urgency": "ความเร่งด่วน",
            "doc_number": "เลขที่หนังสือ",
            "title": "เรื่อง",
            "doc_date": "ลงวันที่",
            "detail": "รายละเอียด",
            "report_to": "เสนอ",
            "operation": "การปฏิบัติ",
            "file": "ไฟล์เอกสาร",
            # 'status':
            # 'author':        '',
            "assigned_sector": "ส่งถึงแผนก",
        }

    # assigned_user = forms.ModelMultipleChoiceField(queryset=None, widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-inline', 'multiple': True}))
