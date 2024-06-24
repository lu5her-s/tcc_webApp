#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : admin.py
# Author            : lu5her <lu5her@mail>
# Date              : Mon Jun, 24 2024, 16:22 176
# Last Modified Date: Mon Jun, 24 2024, 16:38 176
# Last Modified By  : lu5her <lu5her@mail>
# -----
from django.contrib import admin
from .models import (
    Operation,
    WorkPlace,
    Team,
    TeamMember,
    OilReimburesment,
    Allowance,
    AllowanceWithdraw,
    AllowanceRefund,
    OperationCar,
    OperationParcelRequest,
    OperationParcelReturn,
    OperationDocument,
)

# Register your models here.


@admin.register(Operation)
class OperationAdmin(admin.ModelAdmin):
    def team_leader(self, obj):
        return obj.team.team_leader if obj.team else "-"

    list_display = ("pk", "type_of_work", "created_by", "team_leader")
    list_filter = ("type_of_work", "created_by")
    list_display_links = ("pk", "type_of_work", "created_by")
    search_fields = ("pk", "type_of_work", "created_by")


admin.site.register(WorkPlace)
admin.site.register(Team)
admin.site.register(TeamMember)
admin.site.register(OilReimburesment)
admin.site.register(Allowance)
admin.site.register(AllowanceWithdraw)
admin.site.register(AllowanceRefund)
admin.site.register(OperationCar)
admin.site.register(OperationParcelRequest)
admin.site.register(OperationParcelReturn)
admin.site.register(OperationDocument)
