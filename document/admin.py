#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : admin.py
# Author            : lu5her <lu5her@mail>
# Date              : Sun Oct, 09 2022, 16:29 282
# Last Modified Date: Mon Oct, 24 2022, 12:14 297
# Last Modified By  : lu5her <lu5her@mail>
from django.contrib import admin

from document.models import (
    Category,
    Depart,
    Document,
    Operator,
)

# Register your models here.


# admin.site.register(Document)
@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = (
        "recieve_number",
        "urgency",
        "doc_number",
        "doc_date",
        "title",
        "category",
        "created_at",
    )
    list_filter = (
        "urgency",
        "doc_number",
        "doc_date",
        "category",
    )
    search_fields = ("doc_number", "title")


@admin.register(Depart)
class DepartAdmin(admin.ModelAdmin):
    list_display = ("document",)  # Customize as needed


@admin.register(Operator)
class OperatorAdmin(admin.ModelAdmin):
    list_display = ("document",)  # Customize as needed


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)  # Customize as needed
