#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : models.py
# Author            : lu5her <lu5her@mail>
# Date              : Wed Sep, 27 2023, 14:11 270
# Last Modified Date: Wed Sep, 27 2023, 14:11 270
# Last Modified By  : lu5her <lu5her@mail>
from django.db import models
from django.contrib.auth.models import User
from account.models import Department, Profile
from asset.models import (
    StockItem
)

# Create your models here.


class RequestBill(models.Model):
    """
    Model representing a request for a bill.

    Attributes:
        user (models.ForeignKey): The user who requested the bill.
        created_at (models.DateTimeField): The date and time when the request was created.
        receiver (models.ForeignKey): The user who will receive the bill, if specified.
        category_request (models.ForeignKey): The category of the item requested.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    receiver = models.ForeignKey(Profile, related_name='bill_receiver', on_delete=models.CASCADE, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='billdepartment')

    class Meta:
        verbose_name_plural = "Request Bills"

    def __str__(self):
        return f'Bill no : {self.pk}'


class RequestItem(models.Model):
    """
    Model representing an item requested for a bill.
    Attributes:
        bill (models.ForeignKey): The bill to which the item is requested.
        item (models.ForeignKey): The item requested.
        quantity (models.PositiveIntegerField): The quantity requested.
        serial_no (models.CharField): The serial number of the item.
    """
    bill = models.ForeignKey(RequestBill, on_delete=models.CASCADE, related_name='billitems')
    item = models.ForeignKey(StockItem, on_delete=models.CASCADE)
    qauntity = models.PositiveIntegerField(default=1)
    # quantity_approve = models.PositiveIntegerField(default=1)
    serial_no = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Request Items"

    def __str__(self):
        return f'{self.bill.pk} - {self.item.category.name} - {self.qauntity}'


class RequestBillDetail(models.Model):
    """
    Model representing the details of a request bill.
    """

    # Define model fields
    quantity_approve = models.PositiveIntegerField(default=1)
    approve_date = models.DateField(null=True, blank=True)
    approved = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)

    # Define model relationships
    bill = models.ForeignKey(RequestBill, on_delete=models.CASCADE, related_name='billdetail')

    class Meta:
        verbose_name_plural = "Request Bill Details"

    def __str__(self):
        return f'{self.bill.pk}/{self.bill.created_at.year+543}'

    def mark_as_approved(self):
        """
        Mark the request bill as paid.
        """
        self.approved = True
        self.approve_date = datetime.date.today()
        self.save()

    def get_payment_status(self):
        """
        Get the payment status of the request bill.
        To do so, check if the bill is paid and return the item to requester.

        Returns:
        - 'Paid' if the bill is paid
        - 'Unpaid' if the bill is not paid
        """
        return 'Paid' if self.is_paid else 'Unpaid'

# Create your models here.
