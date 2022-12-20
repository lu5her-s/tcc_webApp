#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : admin.py
# Author            : lu5her <lu5her@mail>
# Date              : Thu Sep, 29 2022, 10:01 272
# Last Modified Date: Tue Dec, 20 2022, 20:55 354
# Last Modified By  : lu5her <lu5her@mail>
from django.contrib import admin

from account.models import Department, LineToken, Profile, Rank, Sector, Position

# Register your models here.

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'rank', 'full_name', 'sector', 'position', 'department')
    list_filter = ('rank', 'sector', 'position')
    search_fields = ('sector', 'position')

    def full_name(self, obj):
        return obj.user.get_full_name()
    full_name.short_description = 'Full Name'


@admin.register(LineToken)
class LineTokenAdmin(admin.ModelAdmin):
    list_display = ('name', 'token')
    list_filter = ('name',)
    search_fields = ('name', 'token')
    list_editable = ('token',)


# admin.site.register(Profile)
admin.site.register(Rank)
admin.site.register(Sector)
admin.site.register(Position)
# admin.site.register(LineToken)
admin.site.register(Department)
