#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : forms.py
# Author            : lu5her <lu5her@mail>
# Date              : Fri Oct, 28 2022, 21:13 301
# Last Modified Date: Fri Nov, 11 2022, 22:58 315
# Last Modified By  : lu5her <lu5her@mail>
from account.models import Profile
from django import forms
from django.forms import widgets

from assign.models import Assign, AssignImage, AssignProgress


class AssignModelChoice(forms.ModelChoiceField):
    def label_form_instance(self, obj):
        if obj.profile.rank:
            return obj.get_full_name()
        else:
            return obj.user.username


class AssignForm(forms.ModelForm):
    """
    Form for assign model

    Attributes:
        queryset:
    """

    def __init__(self, current_user, *args, **kwargs):
        super(AssignForm, self).__init__(*args, **kwargs)
        # user = User.objects.get(user=current_user)
        self.fields["assigned_to"].queryset = Profile.objects.exclude(pk=current_user)

    class Meta:
        model = Assign
        fields = (
            "title",
            "body",
            "author",
            "assigned_to",
        )
        widgets = {
            "title": widgets.TextInput(attrs={"class": "form-control"}),
            "body": widgets.Textarea(attrs={"class": "form-control"}),
            "assigned_to": widgets.Select(
                attrs={"class": "form-select", "placeholder": "เลือกผู้ปฏิบัติงาน"}
            ),
            "author": widgets.HiddenInput(
                attrs={"class": "form-control", "id": "author"}
            ),
        }
        labels = {
            "title": "ชื่อเรื่อง",
            "body": "รายละเอียด",
            "author": "ผู้เขียน",
            "assigned_to": "มอบงานหมายให้",
        }


class ProgressForm(forms.ModelForm):
    """
    Form for update progress

    Attributes:
        queryset:
    """

    class Meta:
        model = Assign
        fields = ("status",)

        widgets = {
            "status": widgets.Select(attrs={"class": "form-select"}),
            #'note': widgets.Textarea(attrs={'class': 'form-control'}),
        }
        labels = {
            "status": "สถานะการดำเนินการ",
        }


class NoteForm(forms.ModelForm):
    """
    Form for update note

    Attributes:
        queryset:
    """

    class Meta:
        model = AssignProgress
        fields = ("note",)

        widgets = {
            "note": widgets.Textarea(attrs={"class": "form-control", "rows": 3}),
        }

        labels = {
            "note": "บันทึก",
        }


class CloseAssignForm(forms.ModelForm):
    """
    Form for close assign
    """

    class Meta:
        model = AssignImage
        fields = ("images",)

        widgets = {
            "images": widgets.FileInput(
                attrs={"class": "form-control", "required": False}
            ),
        }
        labels = {
            "images": "ภาพการทำงาน",
        }
