#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : models.py
# Author            : lu5her <lu5her@mail>
# Date              : Thu Apr, 18 2024, 18:51 109
# Last Modified Date: Fri Apr, 19 2024, 16:36 110
# Last Modified By  : lu5her <lu5her@mail>
# -----
from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User

from account.models import Department

# Create your models here.


# function for save image param instance and and filename
def stock_image(instance, filename: str) -> str:
    """upload_image_path.

    :param instance:get instance from StockItem
    :param filename:get filename to set folder
    """
    return f"StockItem/{instance.stock_item.item_name}/{filename}"


# class categories for stock
class Category(models.Model):
    """Category."""

    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(
        upload_to="StockItem/Categories/", null=True, blank=True)

    def __str__(self):
        return f"{self.name}"


# class for supplier for stock
class Supplier(models.Model):
    """Supplier."""

    name = models.CharField(max_length=50)
    address = models.TextField()
    contact_no = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.contact_no}"


class Network(models.Model):
    ''' for network detail have fields : name, ip_addr, description '''

    name = models.CharField(max_length=50)
    ip_addr = models.GenericIPAddressField()
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.ip_addr}"


class Manufacturer(models.Model):
    """
    Manufacturer. for item description
    """

    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class StockItemManager(models.Manager):
    """StockItemManager."""

    def get_queryset(self):
        return super().get_queryset().filter(status=StockItem.Status.AVAILABLE)


class StockItem(models.Model):
    """StockItem."""

    class Status(models.TextChoices):
        """Status."""

        AVAILABLE = 'AVAILABLE', 'พร้อมใช้งาน'
        IN_USE = 'IN_USE', 'กำลังใช้งาน'
        UNDER_MAINTENANCE = 'UNDER_MAINTENANCE', 'ซ่อมบำรุง'
        DISPOSED = 'DISPOSED', 'จำหน่าย'
        CHECK = 'CHECK', 'ตรวจสอบ'
        HOLD = 'HOLD', 'จอง'
        ON_HAND = 'ON_HAND', 'เคลื่อนไหว'

    item_name = models.CharField(max_length=50)
    serial = models.CharField(max_length=50, unique=True, null=True, blank=True)
    description = models.TextField()
    supplier = models.ForeignKey(
        Supplier, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    # location   = models.CharField(max_length=255, null=True, blank=True)
    stock_control = models.ForeignKey(
        Department, on_delete=models.CASCADE, null=True, blank=True, related_name='stock_control')
    location_install = models.ForeignKey(
        Department, on_delete=models.CASCADE, null=True, blank=True, related_name='location_setup')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    manufacturer = models.ForeignKey(
        Manufacturer, on_delete=models.CASCADE, null=True, blank=True)
    model_no = models.CharField(max_length=50, null=True, blank=True)
    part_no = models.CharField(max_length=50, null=True, blank=True)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    network = models.ForeignKey(
        Network, on_delete=models.CASCADE, null=True, blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.AVAILABLE)
    count_text = models.CharField(max_length=50, null=True, blank=True)

    objects = models.Manager()  # default Manager
    available = StockItemManager()  # Custom manager filter available stock_item

    def __str__(self):
        return f"{self.item_name} Serial: {self.serial} Status: {self.status} Location: {self.stock_control}"

    def get_absolute_url(self):
        return reverse('asset:stockitem_detail', kwargs={'pk': self.pk})


class StockItemImage(models.Model):
    """StockItemImage."""

    stock_item = models.ForeignKey(StockItem, on_delete=models.CASCADE, related_name='images')
    images = models.ImageField(upload_to=stock_image)

    def __str__(self):
        return f"{self.stock_item.item_name} - { self.images.name }"


class ItemLocation(models.Model):
    """ItemLocation."""

    item = models.ForeignKey(StockItem, on_delete=models.CASCADE)
    location = models.ForeignKey(Department, on_delete=models.CASCADE)


class ItemOnHand(models.Model):
    """ItemOnHand."""

    item = models.ForeignKey(StockItem, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_done = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.item.item_name} - {self.user.get_full_name()}"


class ItemHistory(models.Model):
    """ItemHistory."""

    item = models.ForeignKey(StockItem, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.item.item_name} - {self.user.get_full_name()}"
