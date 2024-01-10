#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : models.py
# Author            : lu5her <lu5her@mail>
# Date              : Wed Sep, 27 2023, 14:11 270
# Last Modified Date: Wed Sep, 27 2023, 14:11 270
# Last Modified By  : lu5her <lu5her@mail>
from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from account.models import Department, Profile
from asset.models import (
    StockItem,
    Category
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

    class BillStatus(models.TextChoices):
        DRAFT = 'DRAFT', 'ร่าง'
        REQUEST = 'REQUEST', 'ขอเบิก'
        IN_PROGRESS = 'IN_PROGRESS', 'กำลังดำเนินการ'
        DONE = 'DONE', 'เสร็จสิ้น'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    stock = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(
        max_length=50,
        choices=BillStatus.choices,
        default=BillStatus.DRAFT
    )
    is_done = models.BooleanField(default=False)
    date_done = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Request Bills"

    def get_absolute_url(self):
        return reverse_lazy('bill_detail', kwargs={'pk': self.pk})

    def mark_as_done(self):
        self.is_done = True
        self.date_done = datetime.now()
        self.save()

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
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    item = models.ForeignKey(StockItem, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    quantity_approve = models.PositiveIntegerField(null=True, blank=True)
    # price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    # quantity_approve = models.PositiveIntegerField(default=1)
    # serial_no = models.CharField(max_length=50, null=True, blank=True)
    paid = models.BooleanField(default=False)
    paid_date = models.DateField(null=True, blank=True)
    recieved = models.BooleanField(default=False)
    recieved_date = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Request Items"

    def total_price(self):
        if self.item.price and self.quantity:
            return self.item.price * self.quantity
        else:
            return None

    def mark_as_recieved(self):
        self.recieved = True
        self.recieved_date = datetime.now()
        self.item.item.status = StockItem.Status.ON_HAND
        self.item.item.save()
        self.save()

    def mark_as_paid(self):
        self.paid = True
        self.paid_date = datetime.now()
        # change status to on_hold
        self.item.item.status = StockItem.Status.ON_HOLD
        self.item.item.save()
        self.save()

    def __str__(self):
        return f'{self.bill.pk}'


class RequestBillDetail(models.Model):
    """
    Model representing the details of a request bill.
    """

    class ApproveStatus(models.TextChoices):
        APPROVED = 'APPROVED', 'อนุมัติ'
        WAIT = 'WAIT', 'รออนุมัติ'
        UNAPPROVED = 'UNAPPROVED', 'ไม่อนุมัติ'

    class RequestCase(models.TextChoices):
        BASIC = 'BASIC', 'ขั้นต้น'
        REPLACE = 'REPLACE', 'ทดแทน'
        BORROW = 'BORROW', 'ยืม'

    class PaidStatus(models.TextChoices):
        PAID = 'PAID', 'เตรียมจ่ายพัสดุ'
        RECIEVED = 'RECEIVED', 'รับพัสดุแล้ว'

    # Define model fields
    approve_date = models.DateTimeField(null=True, blank=True)
    approve_status = models.CharField(
        max_length=50,
        choices=ApproveStatus.choices,
        default=ApproveStatus.WAIT
    )
    approver = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    receiver = models.ForeignKey(Profile, related_name='bill_receiver', on_delete=models.CASCADE, null=True, blank=True)
    received_at = models.DateTimeField(null=True, blank=True)
    paid_status = models.CharField(
        max_length=50,
        choices=PaidStatus.choices,
        null=True,
        blank=True
    )
    paider = models.ForeignKey(User, related_name='bill_paider', on_delete=models.CASCADE, null=True, blank=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    request_case = models.CharField(
        max_length=50,
        choices=RequestCase.choices,
        default=RequestCase.BASIC
    )
    item_type = models.CharField(max_length=50, null=True, blank=True, default='2 และ 4')
    item_control = models.CharField(max_length=50, null=True, blank=True, default='ส.')
    money_type = models.CharField(max_length=50, null=True, blank=True)
    job_no = models.CharField(max_length=50, null=True, blank=True)
    request_reference = models.CharField(max_length=50, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    agent = models.ForeignKey(User, related_name='bill_agent', on_delete=models.CASCADE, null=True, blank=True)
    request_approve_date = models.DateTimeField(null=True, blank=True)

    # Define model relationships
    bill = models.OneToOneField(RequestBill, on_delete=models.CASCADE, related_name='billdetail')

    class Meta:
        verbose_name_plural = "Request Bill Details"

    def __str__(self):
        return f'{self.bill.pk}/{self.bill.created_at.year+543}'

    def mark_as_approved(self, user):
        """
        Mark the approved date if approve_status update to APPROVE.
        """
        if self.approve_status == RequestBillDetail.ApproveStatus.APPROVE:
            self.approve_date = datetime.now()
            self.approver = user
            self.save()

    def mark_as_paid(self, user):
        """
        Mark the paid date if approve_status update to PAID.
        """
        self.paid_status = RequestBillDetail.PaidStatus.PAID
        self.paid_at = datetime.now()
        self.paider = user
        self.save()

    def add_request_approve_date(self):
        self.request_approve_date = datetime.now()
        self.save()


class BillNote(models.Model):
    bill = models.OneToOneField(RequestBill, on_delete=models.CASCADE)
    note = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity_check = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Bill Notes"

    def __str__(self):
        return f'{self.bill.pk}/{self.created_at.year+543} - {self.user}'


class RejectBillNote(models.Model):
    bill = models.OneToOneField(RequestBill, on_delete=models.CASCADE)
    note = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Reject Bill Notes"

    def __str__(self):
        return f'{self.bill.pk}/{self.created_at.year+543} - {self.user}'
