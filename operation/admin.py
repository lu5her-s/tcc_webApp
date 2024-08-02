#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : admin.py
# Author            : lu5her <lu5her@mail>
# Date              : Mon Jun, 24 2024, 16:22 176
# Last Modified Date: Wed Jul, 03 2024, 16:30 185
# Last Modified By  : lu5her <lu5her@mail>
# -----
from django.contrib import admin
from .models import (
    Operation,
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
    Task,
)

# Register your models here.


@admin.register(Operation)
class OperationAdmin(admin.ModelAdmin):
    def team_leader(self, obj):
        return (
            obj.team.first().team_leader.profile if obj.team.get(operation=obj) else "-"
        )

    def operation_no(self, obj):
        return f"{obj.pk}/{obj.created_at.year+543}"

    list_display = ("operation_no", "type_of_work", "created_by", "team_leader")
    list_filter = ("type_of_work", "created_by")
    list_display_links = ("operation_no",)
    search_fields = ("pk", "type_of_work", "created_by")


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
admin.site.register(Task)
