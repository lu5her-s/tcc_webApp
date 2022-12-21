#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : forms.py
# Author            : lu5her <lu5her@mail>
# Date              : Thu Sep, 29 2022, 15:09 272
# Last Modified Date: Thu Dec, 22 2022, 00:16 356
# Last Modified By  : lu5her <lu5her@mail>
from django import forms
from django.forms import widgets
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User

from account.models import Sector, Rank, Position, Profile, LineToken


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
                'first_name',
                'last_name',
                'email'
                )
        labels = {
                'first_name': 'ชื่อ',
                'last_name':  'นามสกุล',
                'email':      'Email'
                }
        widgets = {
                'first_name': forms.TextInput(attrs  = {'class':  'form-control'}),
                'last_name':  forms.TextInput(attrs  = {'class':  'form-control'}),
                'email':      forms.EmailInput(attrs = {'class': 'form-control'})
                }

class ProfileForm(forms.ModelForm):
    class Meta:
        model   = Profile
        fields  = (
            'rank',
            'position',
            'sector',
            # 'place',
            'phone',
            'image',
            'about',
            'address',
            'twitter',
            'facebook',
            'instagram',
            'line_id',
            'line_token',
            'department',
        )
        exclude = ['password']

        labels  = {
                'rank':       'ยศ',
                'position':   'ตำแหน่ง',
                'sector':     'สังกัด',
                # 'place':    'หน่วย',
                'department': 'สถานที่ทำงาน',
                'phone':      'หมายเลขโทรศัพท์',
                'image':      'รูปประจำตัว',
                'about':      'เกี่ยวกับ',
                'address':    'ที่อยู่',
                'twitter':    'Twitter',
                'facebook':   'Facebook',
                'instagram':  'Instagram',
                'line_id':    'Line ID',
                'line_token': 'Line Token',
                }
        widgets = {
                'rank':       widgets.Select(attrs={'class':           'form-select'}),
                'position':   forms.Select(attrs={'class':             'form-select'}),
                'sector':     forms.Select(attrs={'class':             'form-select'}),
                # 'place':    forms.TextInput(attrs={'class':          'form-control', 'placeholder': 'เช่น สทค.มทบ...'}),
                'department': forms.Select(attrs={'class':             'form-select', 'placeholder':  'เช่น สทค.มทบ.., คลัง..'}),
                'phone':      forms.TextInput(attrs={'class':          'form-control'}),
                'image':      forms.ClearableFileInput(attrs={'class': 'form-control'}),
                'about':      forms.Textarea(attrs={'class':           'form-control'}),
                'address':    forms.TextInput(attrs={'class':          'form-control'}),
                'twitter':    forms.TextInput(attrs={'class':          'form-control'}),
                'facebook':   forms.TextInput(attrs={'class':          'form-control'}),
                'instagram':  forms.TextInput(attrs={'class':          'form-control'}),
                'line_id':    forms.TextInput(attrs={'class':          'form-control'}),
                'line_token': forms.TextInput(attrs={'class':          'form-control'}),
                }


class RankForm(forms.ModelForm):
    class Meta:
        model = Rank
        fields = ('name',)
        labels = {
                'name' : 'ชั้นยศ',
                }
        widgets = {
                'name' : forms.TextInput(attrs={'class': 'form-control w3-input', 'placeholder': 'ชื่อเต็ม เช่น พันเอก, จ่าสิบเอก...'}),
                }


class SectorForm(forms.ModelForm):
    class Meta:
        model  = Sector
        fields = ('name',)
        labels = {
                'name': 'สังกัด',
                }
        widgets = {
                'name' : forms.TextInput(attrs={'class': 'form-control w3-input', 'placeholder': 'สังกัด เช่น ส่วนกลาง, ปก.ทภ...'}),
                }

class PositionForm(forms.ModelForm):
    class Meta:
        model  = Position
        fields = ('name',)
        labels = {
                'name' : 'ตำแหน่ง',
                }
        widgets = {
                'name' : forms.TextInput(attrs={'class': 'form-control w3-input', 'placeholder': 'ตำแหน่ง'}),
                }

class LineTokenForm(forms.ModelForm):
    class Meta:
        model  = LineToken
        fields = ('name', 'token', 'note')
        labels = {
                'name':  'ชื่อโทเคน',
                'token': 'Token',
                'note':  'หมายเหตุ',
                }
        widgets = {
                'name':  forms.TextInput(attrs={'class': 'w3-input', 'placeholder': 'ชื่อโทเคน'}),
                'token': forms.TextInput(attrs={'class': 'w3-input', 'placeholder': 'Line token...'}),
                'note':  forms.Textarea(attrs={'class':  'w3-input'})
                }

