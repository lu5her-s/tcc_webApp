#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : models.py
# Author            : lu5her <lu5her@mail>
# Date              : Mon Jun, 24 2024, 13:52 176
# Last Modified Date: Tue Aug, 20 2024, 17:42 233
# Last Modified By  : lu5her <lu5her@mail>
# -----
import os
from datetime import datetime
from django.contrib.auth.models import User
from django.db import models
from account.models import Department
from car.models import CarBooking
from parcel.models import ParcelRequest, ParcelReturn

# Create your models here.


class Operation(models.Model):
    """
    Operation work flow

    Attributes:
        type_of_work: ประเภทของงาน
        other_type: อื่น ๆ
        description: รายละเอียด
        start_date: วันเริ่ม
        end_date: วันสิ้นสุด
        approve_status: สถานะการอนุมัติ
        operation_status: สถานะของใบงาน
        created_by: สร้างโดย
        created_at: สร้างเมื่อ
        done_date: วันสิ้นสุด
        approve_start_date: วันอนุมัติเปิดงาน
        approver_start: ผู้อนุมัติเปิดงาน
        approve_close_date: วันอนุมัติปิดงาน
        approver_close: ผุ้อนุมัติปิดงาน
        own_car: การใช้ยานพาหนะของตนเอง
        is_deleted: การลบ
    """

    class TypeOfWork(models.TextChoices):
        """
        Description for type_of_work

        Attributes:
            BROADCAST_RADIO:
            SATTELITE:
            FIBER_OPTIC:
            DATA_COMMUNICATION:
            AIR_CONDITION:
            OTHER:
        """

        BROADCAST_RADIO = "BR", "วิทยุถ่ายทอด"
        SATTELITE = "SAT", "ดาวเทียม"
        FIBER_OPTIC = "FO", "ใยแก้วนำแสง"
        DATA_COMMUNICATION = "DC", "สื่อสารข้อมูล"
        AIR_CONDITION = "AC", "เครื่องปรับอากาศ"
        OTHER = "OT", "อื่นๆ"

    class ApproveStatus(models.TextChoices):
        """
        Description for approve_status

        Attributes:
            APPROVE:
            WAIT_OPEN:
            WAIT_CLOSE:
            CLOSED:
            REJECT:
        """

        APPROVE = "AP", "อนุมัติ"
        WAIT_OPEN = "WO", "รออนุมัติเปิดงาน"
        WAIT_CLOSE = "WC", "รออนุมัติปิดงาน"
        CLOSED = "CL", "ปิดงาน"
        REJECT = "RJ", "ไม่อนุมัติ"

    class OperationStatus(models.TextChoices):
        """
        Description for operation_status

        Attributes:
            WAIT:
            PROGRESS:
            DONE:
            LEADER:
            DRAFT:
        """

        WAIT = "WA", "รอดำเนินการ"
        PROGRESS = "IP", "กำลังดำเนินการ"
        DONE = "DO", "เสร็จสิ้น"
        LEADER = "LD", "หัวหน้าชุดตรวจสอบ"
        DRAFT = "DF", "ร่าง"

    type_of_work = models.CharField(
        max_length=3, choices=TypeOfWork.choices, default=TypeOfWork.OTHER
    )
    other_type = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    approve_status = models.CharField(
        max_length=2, choices=ApproveStatus.choices, null=True, blank=True
    )
    operation_status = models.CharField(
        max_length=2, choices=OperationStatus.choices, default=OperationStatus.DRAFT
    )
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="created_by"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    done_date = models.DateTimeField(null=True, blank=True)
    approve_start_date = models.DateField(null=True, blank=True)
    approver_start = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="approver_start",
    )
    approve_close_date = models.DateField(null=True, blank=True)
    approver_close = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="approver_close",
    )
    own_car = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.pk} {self.type_of_work} at {self.created_at} ({self.operation_status})"


class Task(models.Model):
    """

    Attributes:
        operation:
        workplace:
        task:
        priority:
        done_date:
        created_by:
        created_at:
        is_done:
        status:
        note:
    """

    class Priority(models.TextChoices):
        CRITICAL = "CR", "ด่วนมาก"
        URGENT = "UR", "ด่วน"
        NORMAL = "NR", "ปกติ"
        OTHER = "OT", "อื่นๆ"

    class Status(models.TextChoices):
        PENDING = "PD", "รอดำเนินการ"
        CLOSED = "CL", "ปิด"

    operation = models.ForeignKey(
        Operation, on_delete=models.CASCADE, related_name="task"
    )
    workplace = models.ForeignKey(
        Department, on_delete=models.CASCADE, related_name="task_workplace"
    )
    task = models.TextField(null=True, blank=True)
    priority = models.CharField(
        max_length=2, choices=Priority.choices, default=Priority.NORMAL
    )
    done_date = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="task_created_by"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_done = models.BooleanField(default=False)

    status = models.CharField(
        max_length=2, choices=Status.choices, default=Status.PENDING
    )
    note = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.task} {self.operation}"


class Team(models.Model):
    operation = models.OneToOneField(
        Operation, on_delete=models.CASCADE, related_name="team"
    )
    team_leader = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="team_leader",
    )
    accepted = models.BooleanField(default=False)
    accepted_date = models.DateTimeField(null=True, blank=True)

    def accept(self):
        self.accepted = True
        self.accepted_date = datetime.now()

    def __str__(self):
        return f"{self.operation}"


class TeamMember(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="members")
    member = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="teams", null=True, blank=True
    )

    def __str__(self):
        return f"Team : {self.team.pk}"


class OilReimburesment(models.Model):
    class OilType(models.TextChoices):
        BENZENE = "BZ", "เบนซิน"
        DIESEL = "DS", "ดีเซล"

    oil_type = models.CharField(
        max_length=2, choices=OilType.choices, null=True, blank=True
    )
    liter_request = models.FloatField(default=0.0)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="oil_request"
    )
    operaion = models.ForeignKey(
        Operation, on_delete=models.CASCADE, related_name="oil_request"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.oil_type} {self.liter_request} - {self.operaion}"


class Allowance(models.Model):
    """
    Allowance model for Create Request Allowance

    Attributes:
        user:
        operation:
        created_at:
        total_withdraw:
        number_of_withdraw:
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="allowance")
    operation = models.OneToOneField(
        Operation, on_delete=models.CASCADE, related_name="allowance"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    total_withdraw = models.FloatField(default=0.0)
    number_of_withdraw = models.IntegerField(default=0)

    def add_total_withdraw(self, amount):
        self.total_withdraw += amount

    def decrease_total_withdraw(self, amount):
        self.total_withdraw -= amount

    def increase_number_of_withdraw(self):
        self.number_of_withdraw += 1

    def decrease_number_of_withdraw(self):
        # update and check if number = 0 delete this Allowance
        self.number_of_withdraw -= 1
        if self.number_of_withdraw == 0:
            self.delete()

    def __str__(self):
        return f"{self.user}: {self.total_withdraw} - {self.operation}"


class AllowanceWithdraw(models.Model):
    """
    Tracking allowance withdraw, to use

    Attributes:
        allowance: F.K. to Allowance class
        date: date to use allowance
        amount: amount of use
    """

    allowance = models.ForeignKey(
        Allowance, on_delete=models.CASCADE, related_name="withdrawals"
    )
    date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    note = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.amount} -- {self.date}"


class AllowanceRefund(models.Model):
    """
    Return Allowance class

    Attributes:
        allowance:
        date:
        refund_amount:
    """

    allowance = models.ForeignKey(
        Allowance, on_delete=models.CASCADE, related_name="refunds"
    )
    date = models.DateTimeField(auto_now=True)
    refund_amount = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.refund_amount} -- {self.date}"


class OperationCar(models.Model):
    """
    Reference car from CarBooking models

    Attributes:
        operation:
        car_booking:
    """

    operation = models.ForeignKey(
        Operation, on_delete=models.CASCADE, related_name="cars"
    )
    car_booking = models.ForeignKey(
        CarBooking, on_delete=models.CASCADE, related_name="operation_car"
    )

    def __str__(self):
        return f"{self.operation}"


class OperationParcelRequest(models.Model):
    operation = models.ForeignKey(
        Operation, on_delete=models.CASCADE, related_name="parcel_requests"
    )
    parcel = models.ForeignKey(
        ParcelRequest,
        on_delete=models.CASCADE,
        related_name="parcel_request",
    )

    def __str__(self):
        return f"{self.operation}"


class OperationParcelReturn(models.Model):
    operation = models.ForeignKey(
        Operation, on_delete=models.CASCADE, related_name="parcel_returns"
    )
    parcel_return = models.ForeignKey(
        ParcelReturn,
        on_delete=models.CASCADE,
        related_name="parcel_return",
    )

    def __str__(self):
        return f"{self.operation}"


def operation_file_path(instance, filename):
    return os.path.join("operation", str(instance.operation.pk), filename)


class OperationDocument(models.Model):
    operation = models.ForeignKey(
        "Operation", on_delete=models.CASCADE, related_name="documents"
    )
    file = models.FileField(upload_to=operation_file_path, null=True, blank=True)

    class Meta:
        verbose_name = "Operation Document"
