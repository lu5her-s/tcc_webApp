#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : admin.py
# Author            : lu5her <lu5her@mail>
# Date              : Thu Sep, 29 2022, 10:01 272
# Last Modified Date: Thu Sep, 29 2022, 10:01 272
# Last Modified By  : lu5her <lu5her@mail>
from django.contrib import admin

from account.models import Profile, Rank, Sector, Position

# Register your models here.

admin.site.register(Profile)
admin.site.register(Rank)
admin.site.register(Sector)
admin.site.register(Position)
