#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : forms.py
# Author            : lu5her <lu5her@mail>
# Date              : Wed Dec, 21 2022, 01:12 355
# Last Modified Date: Wed Dec, 21 2022, 01:20 355
# Last Modified By  : lu5her <lu5her@mail>
from django import forms

from asset.models import (
    Category,
    Supplier,
    Network,
)

# ModelForm for categorie
class CategoryForm(forms.ModelForm):
    """CategoryForm."""

    class Meta:
        model = Category
        fields = ('name', 'description', 'image',)
        labels = {
            'name': 'ประเภทสินทรัพย์',
            'description': 'รายละเอียด',
            'image': 'รูปภาพ',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }


# ModelForm for supplier
class SupplierForm(forms.ModelForm):
    """SupplierForm."""
    class Meta:
        model = Supplier
        fields = ('name', 'address', 'contact_no',)
        labels = {
            'name': 'ชื่อผู้จัดจำหน่าย',
            'address': 'ที่อยู่',
            'contact_no': 'เบอร์โทรศัพท์',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control'}),
            'contact_no': forms.TextInput(attrs={'class': 'form-control', 'pattern':'[0-9]{10}'}),
        }


# ModelForm For Network
class NetworkForm(forms.ModelForm):
    class Meta:
        model = Network
        fields = ('name', 'ip_addr', 'description',)
        labels = {
            'name': 'ชื่อเครือข่าย',
            'ip_addr': 'ที่อยู่ IP',
            'description': 'รายละเอียด',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'ip_addr': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }
