#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : forms.py
# Author            : lu5her <lu5her@mail>
# Date              : Fri Oct, 28 2022, 21:13 301
# Last Modified Date: Thu Nov, 03 2022, 09:39 307
# Last Modified By  : lu5her <lu5her@mail>
from django import forms
from django.forms import widgets
# from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from account.models import Profile

from account.models import LineToken

from assign.models import Assign, AssignImage, AssignProgress

#class LineTokenMultiple(forms.ModelMultipleChoiceField):
    #def label_form_instance(self, obj: LineToken) -> str:
        #return obj.name

class AssignModelChoice(forms.ModelChoiceField):
    def label_form_instance(self, obj):
        if obj.profile.rank:
            return obj.get_full_name()
        else:
            return obj.user.username

class AssignForm(forms.ModelForm):
    #images = forms.ImageField(widget=forms.ClearableFileInput(attrs={'class': 'w3-input', 'multiple': True}), label="รูปภาพ", required=False)
    #tokens = LineTokenMultiple(
        #queryset=LineToken.objects.all(),
        #label="การแจ้งเตือน",
        #widget=widgets.CheckboxSelectMultiple(),
        #required=False
    #)
    # assigned_to = AssignModelChoice(
            # queryset=Profile.objects.all(),
            # label='มอบงานหมายให้',
            # #widget=widgets.Select(attrs={'class': 'form-control'})
            # )

    def __init__(self, current_user, *args, **kwargs):
        super(AssignForm, self).__init__(*args, **kwargs)
        # user = User.objects.get(user=current_user)
        self.fields['assigned_to'].queryset = Profile.objects.exclude(id=current_user.id)

    class Meta:
        model   = Assign
        fields  = ('title', 'body', 'author', 'assigned_to',)
        widgets = {
                'title'       : widgets.TextInput(attrs   = {'class': 'form-control'}),
                'body'        : widgets.Textarea(attrs    = {'class': 'form-control'}),
                # 'body'        : RichTextField(),
                # 'detail' : CKEditorWidget(attrs={'class': 'w3-input'}),
                'assigned_to' : widgets.Select(attrs      = {'class': 'form-select', 'placeholder': 'เลือกผู้ปฏิบัติงาน'}),
                'author'      : widgets.HiddenInput(attrs = {'class': 'form-control', 'id': 'author'}),
                }
        labels = {
                'title'  : 'ชื่อเรื่อง',
                'body'   : 'รายละเอียด',
                'author' : 'ผู้เขียน',
                }

class ProgressForm(forms.ModelForm):
    class Meta:
        model = Assign
        fields = ('status',)

        widgets = {
                'status' : widgets.Select(attrs={'class': 'form-select'}),
                #'note': widgets.Textarea(attrs={'class': 'form-control'}),
                }
        labels = {
                'status' : 'สถานะการดำเนินการ',
                }

class NoteForm(forms.ModelForm):
    class Meta:
        model = AssignProgress
        fields = ('note',)

        widgets = {
            'note': widgets.Textarea(attrs={'class': 'form-control', 'rows':3}),
        }

        labels = {
            'note': 'บันทึก',
        }

class CloseAssignForm(forms.ModelForm):
    class Meta:
        model = AssignImage
        fields = ('images',)

        widgets = {
            'images': widgets.FileInput(attrs={'class': 'form-control', 'required': False}),
        }
        labels = {
            'images': 'ภาพการทำงาน',
        }
