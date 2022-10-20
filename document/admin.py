#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : admin.py
# Author            : lu5her <lu5her@mail>
# Date              : Sun Oct, 09 2022, 16:29 282
# Last Modified Date: Tue Oct, 18 2022, 11:53 291
# Last Modified By  : lu5her <lu5her@mail>
from django.contrib import admin

from document.models import (
    Category,
    Document,
    Department,
    Operator,
)

# Register your models here.

# admin.site.register(Document)
@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('urgency', 'doc_number', 'title', 'doc_date',)
    list_filter = ('urgency', 'doc_number', 'title', 'doc_date',)
    search_fields = ('doc_number', 'title')

admin.site.register(Department)
admin.site.register(Operator)
admin.site.register(Category)
