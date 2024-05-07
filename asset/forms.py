#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : forms.py
# Author            : lu5her <lu5her@mail>
# Date              : Wed Dec, 21 2022, 01:12 355
# Last Modified Date: Fri Apr, 19 2024, 16:15 110
# Last Modified By  : lu5her <lu5her@mail>
from django import forms

from account.models import Department

from asset.models import (
    Category,
    StockItem,
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


# ModelForm for StockItem
class StockItemForm(forms.ModelForm):
    images = forms.ImageField(
        widget=forms.ClearableFileInput(
            attrs={
                'class': 'form-control',
                'multiple': True,
            }
        ),
        label="ภาพพัสดุ",
        required=False,
    )
    class Meta:
        model = StockItem
        fields = (
            'category',
            'item_name',
            'manufacturer',
            'serial',
            'description',
            'model_no',
            'part_no',
            'price',
            'supplier',
            'price',
            'network',
            'location_install',
            'stock_control',
            'images',
        )

        labels = {
            'category':     'ประเภท',
            'item_name':    'ชื่อสินค้า',
            'manufacturer': 'ผู้ผลิต',
            'serial':       'หมายเลขซีเรียล',
            'description':  'รายละเอียด',
            'model_no':     'รุ่น',
            'part_no':      'หมายเลขอะไหล่',
            'price':        'ราคา',
            'supplier':     'ผู้จัดจำหน่าย',
            'network':      'เครือข่าย',
            'location_install':     'สถานที่ติดตั้ง',
            'stock_control': 'คลัง',
        }

        widgets = {
            'category':     forms.Select(attrs={'class': 'form-select'}),
            'item_name':    forms.TextInput(attrs={'class': 'form-control'}),
            'manufacturer': forms.Select(attrs={'class': 'form-select'}),
            'serial':       forms.TextInput(attrs={'class': 'form-control'}),
            'description':  forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'model_no':     forms.TextInput(attrs={'class': 'form-control'}),
            'part_no':      forms.TextInput(attrs={'class': 'form-control'}),
            'price':        forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'step': 0.01}),
            'supplier':     forms.Select(attrs={'class': 'form-select'}),
            'network':      forms.Select(attrs={'class': 'form-select'}),
            # 'location':     forms.Select(attrs={'class': 'form-select'}),
            'location_install':     forms.HiddenInput(attrs={'class': 'form-select'}),
            'stock_control': forms.Select(attrs={'class': 'form-select'}),
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['stock_control'].choices = [(c.id, c.name) for c in Department.objects.filter(name__startswith='คลัง')]
