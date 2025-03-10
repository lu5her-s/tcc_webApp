#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : models.py
# Author            : lu5her <lu5her@mail>
# Date              : Wed Nov, 02 2022, 14:37 306
# Last Modified Date: Mon Jun, 24 2024, 15:39 176
# Last Modified By  : lu5her <lu5her@mail>
import datetime

from account.models import Profile
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.db import models

# Create your models here.


def get_image_name(instance: object, filename: str) -> str:
    """get_image_name.

    :param instance:object
    :param filename:str
    for store image for car
    """
    car_number = instance.number.replace(" ", "_").replace("-", "_")

    return f"Car/{car_number}/{filename}"


def get_image_fix(instance: object, filename: str) -> str:
    """get_image_fix.

    :param instance:
    :type instance: object
    :param filename:
    :type filename: str
    :rtype: str
    """
    car_number = instance.car.number
    return f"Car/Fix/{car_number}/{filename}"


class Car(models.Model):
    """
    Car. detail for car general data for car

    Attributes:
        car_type:
        number:
        manufacturer:
        color:
        capacity:
        fuel_max:
        fuel_rate:
        fuel_now:
        status:
        responsible_man:
        created_at:
        updated_at:
        mile_now:
        car_avatar:
    """

    class Type(models.TextChoices):
        VAN = "van", "รถตู้"
        TRUCK = "truck", "รถบรรทุก"
        BUS = "bus", "รถบัส"
        WAGON = "wagon", "รถระบะ"
        OTHER = "other", "อื่นๆ"

    class Status(models.TextChoices):
        READY = "ready", "พร้อมใช้งาน"
        PENDING = "pending", "จอง"
        WAIT = "wait", "รอดำเนินการ"
        INUSE = "inuse", "ใช้งานอยู่"
        FIX = "fix", "ซ่อมบำรุง"
        NOT_READY = "not_ready", "ไม่พร้อมใช้งาน"

    car_type = models.CharField(
        max_length=200,
        choices=Type.choices,
        default=Type.VAN,
        null=True,
        blank=True,
    )
    number = models.CharField(max_length=50)
    manufacturer = models.CharField(max_length=200, null=True, blank=True)
    color = models.CharField(max_length=50, null=True, blank=True)
    capacity = models.PositiveIntegerField(default=2)
    fuel_max = models.FloatField(default=40.0)
    fuel_rate = models.FloatField(default=0.0)
    fuel_now = models.FloatField(default=0.0)
    status = models.CharField(
        max_length=200,
        choices=Status.choices,
        default=Status.READY,
        null=True,
        blank=True,
    )
    responsible_man = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="responsible_man"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    mile_now = models.FloatField(default=0.0)
    car_avatar = models.ImageField(upload_to=get_image_name, null=True, blank=True)

    class Meta:
        verbose_name = "Car"
        verbose_name_plural = "Car"

    def __str__(self) -> str:
        fuel_now = self.fuel_now
        fuel_max = self.fuel_max
        percent = (fuel_now / fuel_max) * 100
        return f"{self.get_car_type_display()} เลขทะเบียน {self.number} สถานภาพเชื้อเพลิง {self.fuel_now}/{self.fuel_max}({percent} %)"


class CarBooking(models.Model):
    """
    CarUse. for request use car init request change status car to pending

    Attributes:
        car:
        requester:
        mission:
        driver:
        passenger:
        controler:
        approver:
        requested_at:
        mile_in:
        mile_out:
        distance:
        return_at:
        fuel_use:
        status:
        created_at:
    """

    class Status(models.TextChoices):
        PENDING = "pending", "รออนุมัติ"
        APPROVE = "approve", "อนุมัติ"
        REJECT = "reject", "ไม่อนุมัติ"
        CANCEL = "cancel", "ยกเลิก"
        DONE = "done", "เสร็จสิ้น"

    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="car_booking")
    requester = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="requester_car"
    )
    mission = models.TextField()
    driver = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="driver", null=True, blank=True
    )
    passenger = models.PositiveIntegerField(default=1)
    controler = models.ForeignKey(
        Profile, on_delete=models.CASCADE, null=True, blank=True
    )
    approver = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="use_approver"
    )
    requested_at = models.DateTimeField()
    mile_in = models.FloatField(null=True, blank=True)
    mile_out = models.FloatField(null=True, blank=True)
    distance = models.FloatField(default=0)
    return_at = models.DateTimeField(null=True, blank=True)
    fuel_use = models.FloatField(default=0.0)
    # DONE: change choice to class textchoices
    status = models.CharField(
        max_length=200,
        choices=Status.choices,
        default=Status.PENDING,
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Car Booking"
        verbose_name_plural = "Car Booking"

    def __str__(self) -> str:
        year: int = datetime.date.today().year + 543
        if self.requester.profile:
            return f"ใบขอใช้รถเลขที่ {self.pk}/{year} - {self.car.number} ผู้ขอใช้ {self.requester.profile.rank} {self.requester.get_full_name()}"
        else:
            return f"ใบขอใช้รถเลขที่ {self.pk}/{year} - {self.car.number} ผู้ขอใช้ {self.requester.get_full_name()}"


class CarFix(models.Model):
    """
    CarFix. request to fix car change status car to in maintenance

    Attributes:
        car:
        issue:
        fix_requester:
        approver:
        requested_at:
        cost_use:
        finished_at:
        approve_status:
        note:
        responsible_man:
        fix_status:
    """

    class Status(models.TextChoices):
        PENDING = "pending", "รอดำเนินการ"
        IN_MAINTENANCE = "in_maintenance", "กําลังซ่อม"
        FINISHED = "finished", "เสร็จสิ้น"

    class ApproveStatus(models.TextChoices):
        PENDING = "pending", "รออนุมัติ"
        APPROVE = "approve", "อนุมัติ"
        REJECT = "reject", "ไม่อนุมัติ"
        CANCEL = "cancel", "ยกเลิก"
        DONE = "done", "เสร็จสิ้น"

    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="car_fix")
    issue = models.TextField(null=True, blank=True)
    # cost_expect = models.PositiveIntegerField(default=0)
    fix_requester = models.ForeignKey(User, on_delete=models.CASCADE)
    approver = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="fix_approver"
    )
    requested_at = models.DateTimeField(auto_now_add=True)
    cost_use = models.PositiveIntegerField(default=0, null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    approve_status = models.CharField(
        max_length=200,
        choices=ApproveStatus.choices,
        default=ApproveStatus.PENDING,
        null=True,
        blank=True,
    )
    note = models.TextField(null=True, blank=True)
    responsible_man = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="responsible",
        null=True,
        blank=True,
    )
    fix_status = models.CharField(
        max_length=200,
        choices=Status.choices,
        default=Status.PENDING,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Car Fix"
        verbose_name_plural = "Car Fix"

    def __str__(self) -> str:
        return f"{self.car.number} ผู้แจ้ง {self.fix_requester.get_full_name()}"


class Refuel(models.Model):
    """
    Refuel for refuel car

    Attributes:
        car:
        refuel:
        mile_refuel:
        refueler:
        refueled_at:
        note:
    """

    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="car_refuel")
    refuel = models.FloatField(default=0.0)
    mile_refuel = models.FloatField(null=True, blank=True)
    refueler = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="refueler"
    )
    refueled_at = models.DateTimeField(auto_now_add=True)
    note = RichTextField(null=True, blank=True)

    class Meta:
        verbose_name = "Refuel"
        verbose_name_plural = "Refuel"

    def __str__(self) -> str:
        return f"{self.car.number} จำนวนน้ำมันที่เติม {self.refuel} ผู้เติม {self.refueler.get_full_name()}"


class CarImage(models.Model):
    """
    Car Image

    Attributes:
        car:
        images:
    """

    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    images = models.ImageField(upload_to=get_image_name, blank=True, null=True)

    class Meta:
        verbose_name = "Car Image"
        verbose_name_plural = "Car Image"

    def __str__(self) -> str:
        return f"{self.car.number}"


class CarFixImage(models.Model):
    """
    Car Fix Image

    Attributes:
        fix:
        images:
    """

    fix = models.ForeignKey(CarFix, on_delete=models.CASCADE)
    images = models.ImageField(upload_to=get_image_fix, blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.fix.car.number}"


class CarAfterFixImage(models.Model):
    """
    Car After Fix Image

    Attributes:
        fix:
        images:
    """

    fix = models.ForeignKey(CarFix, on_delete=models.CASCADE)
    images = models.ImageField(upload_to=get_image_fix, blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.fix.car.number}"
