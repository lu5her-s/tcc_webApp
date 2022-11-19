#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : models.py
# Author            : lu5her <lu5her@mail>
# Date              : Wed Nov, 02 2022, 14:37 306
# Last Modified Date: Thu Nov, 17 2022, 21:12 321
# Last Modified By  : lu5her <lu5her@mail>
import datetime
from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

from account.models import Profile

# Create your models here.


def get_image_name(instance : object, filename : str) -> str:
    """get_image_name.

    :param instance:object
    :param filename:str
    for store image for car
    """
    car_number = instance.car.number
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


class ApproveStatus(models.Model):
    """RequestStatus. for track status when request user, fix, re_fuel"""

    name = models.CharField(max_length=200)

    class Meta:
        verbose_name = 'Approve Status'
        verbose_name_plural = 'Approve Status'

    def __str__(self) -> str:
        return f"{self.name}"


class CarType(models.Model):
    """CarType. for type of car : van, truck etc."""

    name = models.CharField(max_length=200)

    class Meta:
        verbose_name = 'Type'
        verbose_name_plural = 'Type'

    def __str__(self) -> str:
        return f"{self.name}"


class CarStatus(models.Model):
    """CarStatus. show status : ready, pending, inuse, fix etc."""

    name = models.CharField(max_length=200)

    class Meta:
        verbose_name = 'Status'
        verbose_name_plural = 'Status'

    def __str__(self) -> str:
        return f"{self.name}"

class Car(models.Model):
    """Car. detail for car general data for car"""

    type = models.ForeignKey(CarType, on_delete=models.CASCADE)
    number = models.CharField(max_length=50)
    manufacturer = models.CharField(max_length=200, null=True, blank=True)
    color = models.CharField(max_length=50, null=True, blank=True)
    capacity = models.PositiveIntegerField(default=2)
    fuel_max = models.FloatField(default=40.0)
    fuel_rate = models.FloatField(default=0.0)
    fuel_now = models.FloatField(default=0.0)
    status = models.ForeignKey(CarStatus, on_delete=models.CASCADE, related_name='car_status')
    responsible_man = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='responsible_man')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    mile_now = models.PositiveIntegerField(default=0)
    car_avatar = models.ImageField(upload_to='Car/', null=True, blank=True)

    class Meta:
        verbose_name = 'Car'
        verbose_name_plural = 'Car'

    def __str__(self) -> str:
        fuel_now = self.fuel_now
        fuel_max = self.fuel_max
        percent = (fuel_now/fuel_max)*100
        return f"{self.type.name} เลขทะเบียน {self.number} สถานภาพเชื้อเพลิง {self.fuel_now}/{self.fuel_max}({percent} %)"


class CarBooking(models.Model):
    """CarUse. for request use car init request change status car to pending"""

    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='car_booking')
    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requester_car')
    mission = models.TextField()
    driver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='driver', null=True, blank=True)
    passenger = models.PositiveIntegerField(default=1)
    controler = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    approver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='use_approver')
    requested_at = models.DateTimeField()
    mile_current = models.PositiveIntegerField(null=True, blank=True)
    distance = models.PositiveIntegerField(default=0)
    return_at = models.DateTimeField(null=True, blank=True)
    fuel_use = models.FloatField(default=0.0)
    approve_status = models.ForeignKey(ApproveStatus, on_delete=models.CASCADE, related_name='use_approve_status')

    class Meta:
        verbose_name = 'Car Booking'
        verbose_name_plural = 'Car Booking'

    def __str__(self) -> str:
        year: int = datetime.date.today().year + 543
        if self.requester.profile:
            return f"ใบขอใช้รถเลขที่ {self.pk}/{year} - {self.car.number} ผู้ขอใช้ {self.requester.profile.rank} {self.requester.get_full_name()}"
        else:
            return f"ใบขอใช้รถเลขที่ {self.pk}/{year} - {self.car.number} ผู้ขอใช้ {self.requester.get_full_name()}"


class CarFix(models.Model):
    """CarFix. request to fix car change status car to in maintenance"""

    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    issue = RichTextField(null=True, blank=True)
    cost_expect = models.PositiveIntegerField(default=0)
    fix_requester = models.ForeignKey(User, on_delete=models.CASCADE)
    approver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='fix_approver')
    requested_at = models.DateTimeField(auto_now_add=True)
    cost_use = models.PositiveIntegerField(default=0)
    finished_at = models.DateTimeField(null=True, blank=True)
    approve_status = models.ForeignKey(ApproveStatus, on_delete=models.CASCADE, related_name='fix_approve_status', null=True, blank=True)
    note = RichTextField(null=True, blank=True)

    class Meta:
        verbose_name = 'Car Fix'
        verbose_name_plural = 'Car Fix'

    def __str__(self) -> str:
        return f"{self.car.number} ผู้แจ้ง {self.fix_requester.get_full_name()}" 


class Refuel(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    refuel = models.PositiveIntegerField(default=0)
    refueler = models.ForeignKey(User, on_delete=models.CASCADE, related_name='refueler')
    refueled_at = models.DateTimeField(auto_now_add=True)
    note = RichTextField(null=True, blank=True)

    class Meta:
        verbose_name = 'Refuel'
        verbose_name_plural = 'Refuel'

    def __str__(self) -> str:
        return f"{self.car.number} จำนวนน้ำมันที่เติม {self.refuel} ผู้เติม {self.get_full_name()}"


class CarImage(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    images = models.ImageField(upload_to='get_image_name', blank=True, null=True)

    class Meta:
        verbose_name = 'Car Image'
        verbose_name_plural = 'Car Image'

    def __str__(self) -> str:
        return f"{self.car.number}"


class CarFixImage(models.Model):
    fix = models.ForeignKey(CarFix, on_delete=models.CASCADE)
    images = models.ImageField(upload_to='get_image_fix', blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.fix.car.number}"
