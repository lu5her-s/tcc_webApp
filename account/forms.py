#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : forms.py
# Author            : lu5her <lu5her@mail>
# Date              : Thu Sep, 29 2022, 15:09 272
# Last Modified Date: Mon May, 26 2025, 15:08 146
# Last Modified By  : lu5her <lu5her@mail>
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import widgets

from account.models import LineToken, Position, Profile, Rank, Sector


# ===== Helpers for DRY code =====
def form_control(attrs=None):
    """
    Shortcut for common form-control class.

    Args:
        attrs (): dict

    Returns:

    """
    base = {"class": "form-control"}
    if attrs:
        base.update(attrs)
    return base


def w3_input(attrs=None):
    """
    Shortcut for common w3-input class.

    Args:
        attrs (): dict

    Returns:

    """
    base = {"class": "w3-input"}
    if attrs:
        base.update(attrs)
    return base


# === abstract base for simple (single-name)  model forms ===
class _SingleNameForm(forms.ModelForm):
    name_placeholder = None
    name_label = None
    name_class = "form-control w3-input"

    class Meta:
        fields = ("name",)
        labels = {}
        widgets = {}

    def __init_subclass__(cls, **kwargd):
        super().__init_subclass__(**kwargd)
        # Setup class attributes after subclass defines them
        if cls.name_label:
            cls.labels = {"name": cls.name_label}
        if cls.name_placeholder:
            cls.Meta.widgets = {
                "name": forms.TextInput(
                    attrs={"class": cls.name_class, "placeholder": cls.name_placeholder}
                )
            }


class UserForm(UserCreationForm):
    """
    Form for creating and updating user information.
    """

    class Meta:
        model = User
        fields = (
            "username",
            "password1",
            "password2",
            "first_name",
            "last_name",
            "email",
        )
        labels = {
            "username": "ชื่อผู้ใช้",
            "password1": "รหัสผ่าน",
            "password2": "ยืนยันรหัสผ่าน",
            "first_name": "ชื่อ",
            "last_name": "นามสกุล",
            "email": "Email",
        }
        widgets = {
            "username": forms.TextInput(attrs=form_control()),
            "password1": forms.PasswordInput(attrs=form_control()),
            "password2": forms.PasswordInput(attrs=form_control()),
            "first_name": forms.TextInput(attrs=form_control()),
            "last_name": forms.TextInput(attrs=form_control()),
            "email": forms.EmailInput(attrs=form_control()),
        }


class ProfileForm(forms.ModelForm):
    """
    Form for creating and updating profile information.
    """

    class Meta:
        model = Profile
        fields = (
            "rank",
            "position",
            "sector",
            "phone",
            "image",
            "about",
            "address",
            "twitter",
            "facebook",
            "instagram",
            "line_id",
            "line_token",
            "department",
        )
        exclude = ["password"]

        labels = {
            "rank": "ยศ",
            "position": "ตำแหน่ง",
            "sector": "สังกัด",
            "department": "สถานที่ทำงาน",
            "phone": "หมายเลขโทรศัพท์",
            "image": "รูปประจำตัว",
            "about": "เกี่ยวกับ",
            "address": "ที่อยู่",
            "twitter": "Twitter",
            "facebook": "Facebook",
            "instagram": "Instagram",
            "line_id": "Line ID",
            "line_token": "Line Token",
        }
        widgets = {
            "rank": widgets.Select(attrs={"class": "form-select"}),
            "position": forms.Select(attrs={"class": "form-select"}),
            "sector": forms.Select(attrs={"class": "form-select"}),
            "department": forms.Select(
                attrs={"class": "form-select", "placeholder": "เช่น สทค.มทบ.., คลัง.."}
            ),
            "phone": forms.TextInput(attrs=form_control()),
            "image": forms.ClearableFileInput(attrs=form_control()),
            "about": forms.Textarea(attrs=form_control()),
            "address": forms.TextInput(attrs=form_control()),
            "twitter": forms.TextInput(attrs=form_control()),
            "facebook": forms.TextInput(attrs=form_control()),
            "instagram": forms.TextInput(attrs=form_control()),
            "line_id": forms.TextInput(attrs=form_control()),
            "line_token": forms.TextInput(attrs=form_control()),
        }


class RankForm(_SingleNameForm):
    """
    Form for creating and updating rank information.
    """

    # class Meta:
    #     model = Rank
    #     fields = ("name",)
    #     labels = {
    #         "name": "ชั้นยศ",
    #     }
    #     widgets = {
    #         "name": forms.TextInput(
    #             attrs={
    #                 "class": "form-control w3-input",
    #                 "placeholder": "ชื่อเต็ม เช่น พันเอก, จ่าสิบเอก...",
    #             }
    #         ),
    #     }
    name_placeholder = "ชื่อเต็ม เช่น พันเอก, จ่าสิบเอก..."
    name_label = "ชั้นยศ"


class SectorForm(_SingleNameForm):
    # class Meta:
    #     model = Sector
    #     fields = ("name",)
    #     labels = {
    #         "name": "สังกัด",
    #     }
    #     widgets = {
    #         "name": forms.TextInput(
    #             attrs={
    #                 "class": "form-control w3-input",
    #                 "placeholder": "สังกัด เช่น ส่วนกลาง, ปก.ทภ...",
    #             }
    #         ),
    #     }
    name_placeholder = "สังกัด เช่น ส่วนกลาง, ปก.ทภ..."
    name_label = "สังกัด"


class PositionForm(_SingleNameForm):
    # class Meta:
    #     model = Position
    #     fields = ("name",)
    #     labels = {
    #         "name": "ตำแหน่ง",
    #     }
    #     widgets = {
    #         "name": forms.TextInput(
    #             attrs={"class": "form-control w3-input", "placeholder": "ตำแหน่ง"}
    #         ),
    #     }
    name_placeholder = "ตำแหน่ง"
    name_label = "ตำแหน่ง"


class LineTokenForm(forms.ModelForm):
    class Meta:
        model = LineToken
        fields = ("name", "token", "note")
        labels = {
            "name": "ชื่อโทเคน",
            "token": "Token",
            "note": "หมายเหตุ",
        }
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "w3-input", "placeholder": "ชื่อโทเคน"}
            ),
            "token": forms.TextInput(
                attrs={"class": "w3-input", "placeholder": "Line token..."}
            ),
            "note": forms.Textarea(attrs=w3_input()),
        }
