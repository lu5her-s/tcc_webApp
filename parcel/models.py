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


class ParcelRequest(models.Model):
    """
    Model representing a request for a bill.

    Attributes:
        user (models.ForeignKey): The user who requested the bill.
        created_at (models.DateTimeField): The date and time when the request was created.
        receiver (models.ForeignKey): The user who will receive the bill, if specified.
        category_request (models.ForeignKey): The category of the item requested.
    """

    class RequestStatus(models.TextChoices):
        DRAFT = 'DRAFT', 'ร่าง'
        REQUEST = 'REQUEST', 'ขอเบิก'
        IN_PROGRESS = 'IN_PROGRESS', 'กำลังดำเนินการ'
        DONE = 'DONE', 'เสร็จสิ้น'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    stock = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(
        max_length=50,
        choices=RequestStatus.choices,
        default=RequestStatus.DRAFT
    )
    is_done = models.BooleanField(default=False)
    date_done = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Parcel Request Bills"

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
    bill = models.ForeignKey(ParcelRequest, on_delete=models.CASCADE, related_name='billitems')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    item = models.ForeignKey(StockItem, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    quantity_approve = models.PositiveIntegerField(default=1)
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

    def mark_as_received(self):
        self.recieved = True
        self.recieved_date = datetime.now()
        self.item.status = StockItem.Status.ON_HAND
        self.item.save()
        self.save()

    def mark_as_paid(self):
        self.paid = True
        self.paid_date = datetime.now()
        # change status to on_hold
        self.item.status = StockItem.Status.HOLD
        self.item.save()
        self.save()

    def __str__(self):
        return f'Bill no : {self.bill.pk} - {self.item.item_name} [quantity: {self.quantity}]'


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
        RECEIVED = 'RECEIVED', 'รับพัสดุแล้ว'

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
    paid_no = models.CharField(max_length=10, null=True, blank=True)

    # Define model relationships
    bill = models.OneToOneField(ParcelRequest, on_delete=models.CASCADE, related_name='billdetail')

    class Meta:
        verbose_name_plural = "Request Bill Details"

    def __str__(self):
        return f'Bill no: {self.bill.pk}/{self.bill.created_at.year+543} - Request User: {self.bill.user}'

    def mark_as_approved(self, user):
        """
        Mark the approved date if approve_status update to APPROVE.
        """
        if self.approve_status == RequestBillDetail.ApproveStatus.APPROVED:
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

    def mark_as_received(self):
        self.received_at = datetime.now()
        self.paid_status = RequestBillDetail.PaidStatus.RECEIVED
        self.save()

class ParcelRequestNote(models.Model):
    bill = models.OneToOneField(ParcelRequest, on_delete=models.CASCADE)
    note = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity_check = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Parcel Request Bill Notes"

    def __str__(self):
        return f'{self.bill.pk}/{self.created_at.year+543} - {self.user}'


class RejectBillNote(models.Model):
    bill = models.OneToOneField(ParcelRequest, on_delete=models.CASCADE)
    note = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Reject Parcel Request Bill Notes"

    def __str__(self):
        return f'{self.bill.pk}/{self.created_at.year+543} - {self.user}'


# For Return Parcel
class ParcelReturn(models.Model):

    class Status(models.TextChoices):
        DRAFT = 'DRAFT', 'ร่าง'
        REQUEST = 'REQUEST', 'ขอคืน'
        WAIT = 'WAIT', 'รอการตรวจสอบ'
        DONE = 'DONE', 'ตรวจสอบเสร็จสิ้น'

    status = models.CharField(
        max_length=50,
        choices=Status.choices,
        default=Status.DRAFT
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    stock_reciever = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True, related_name='stock_reciever')
    department_return = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True, related_name='department_return')
    is_done = models.BooleanField(default=False)
    date_done = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Parcel Return Bills"

    def __str__(self):
        return f'{self.pk}/{self.created_at.year+543} - {self.user}'


class ParcelReturnDetail(models.Model):
    class ApproveStatus(models.TextChoices):
        APPROVED = 'APPROVED', 'อนุมัติ'
        WAIT = 'WAIT', 'รออนุมัติ'
        UNAPPROVED = 'UNAPPROVED', 'ไม่อนุมัติ'

    class ReturnCase(models.TextChoices):
        UWT = 'Wear and tear', 'ใช้ในราชการไม่ได้เนื่องจากชำรุดตามสภาพ'
        UAI = 'Investigation report', 'ใช้ในราชการไม่ได้ตามรายงานการสอบสวน'
        UCD = 'Compensation', 'ใช้ในราชการไม่ได้ซึ่งต้องชดใช้ค่าเสียหาย'
        S = 'Serviceable', 'ใช้ในราชการได้'
        E = 'Exess', 'เกินอัตรา'
        L = 'On loan', 'ยืม'

    class ReturnStatus(models.TextChoices):
        WAIT = 'WAIT', 'รอการตรวจสอบ'
        RETURNED = 'RETURNED', 'ส่งคืนแล้ว'

    # Define model fields
    approve_date = models.DateTimeField(null=True, blank=True)
    approve_status = models.CharField(
        max_length=50,
        choices=ApproveStatus.choices,
        default=ApproveStatus.WAIT
    )
    approver = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    returned_at = models.DateTimeField(null=True, blank=True)
    return_status = models.CharField(
        max_length=50,
        choices=ReturnStatus.choices,
        null=True,
        blank=True
    )
    receiver = models.ForeignKey(User, related_name='parcel_receiver', on_delete=models.CASCADE, null=True, blank=True)
    return_case = models.CharField(
        max_length=50,
        choices=ReturnCase.choices,
        null=True,
        blank=True
    )
    item_type = models.CharField(max_length=50, null=True, blank=True, default='2 และ 4')
    item_control = models.CharField(max_length=50, null=True, blank=True, default='ส.')
    money_type = models.CharField(max_length=50, null=True, blank=True)
    job_no = models.CharField(max_length=50, null=True, blank=True)
    request_reference = models.CharField(max_length=50, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    return_approve_date = models.DateTimeField(null=True, blank=True)
    return_no = models.CharField(max_length=10, null=True, blank=True)
    controler = models.ForeignKey(User, related_name='bill_controler', on_delete=models.CASCADE, null=True, blank=True)

    # Define model relationships
    bill = models.OneToOneField(ParcelReturn, on_delete=models.CASCADE, related_name='billdetail')

    class Meta:
        verbose_name_plural = "Parcel Return Bill Details"

    def __str__(self):
        return f'Bill no: {self.bill.pk}/{self.bill.created_at.year+543} - Request User: {self.bill.user}'

    def mark_as_approved(self, user):
        """
        Mark the approved date if approve_status update to APPROVE.
        """
        if self.approve_status == ParcelReturnDetail.ApproveStatus.APPROVED:
            self.approve_date = datetime.now()
            self.approver = user
            self.save()

    def mark_as_return(self, user):
        """
        Mark the paid date if approve_status update to PAID.
        """
        self.return_status = ParcelReturnDetail.ReturnStatus.RETURNED
        self.returned_at = datetime.now()
        self.receiver = user
        self.save()

    def add_return_approve_date(self):
        self.return_approve_date = datetime.now()
        self.save()


class RejectReturnBillNote(models.Model):
    bill = models.OneToOneField(ParcelReturn, on_delete=models.CASCADE)
    note = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    verbose_name_plural = "Reject Parcel Return Bill Notes"

    def __str__(self):
        return f'{self.bill.pk}/{self.created_at.year+543} - {self.user}'

class ParcelReturnBillNote(models.Model):
    bill = models.OneToOneField(ParcelReturn, on_delete=models.CASCADE)
    note = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    verbose_name_plural = "Parcel Return Bill Notes"

    def __str__(self):
        return f'{self.bill.pk}/{self.created_at.year+543} - {self.user}'

class ParcelReturnItem(models.Model):
    bill = models.ForeignKey(ParcelReturn, on_delete=models.CASCADE, related_name='return_bill')
    item = models.ForeignKey(StockItem, on_delete=models.CASCADE, related_name='return_item')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    verbose_name_plural = "Parcel Return Items"

    def __str__(self):
        return f'{self.bill.pk}/{self.created_at.year+543} - {self.item}'
