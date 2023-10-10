from assign.views import accepted
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor.fields import RichTextField

from asset.models import StockItem
from account.models import Profile
from car.models import CarBooking

# Create your models here.


def inform_image(instance, filename):
    """inform_image.

        :param instance: instance inform class
        :param filename: get filename for set path
        """
    return f"Inform/{instance.inform.pk}/{filename}"


class Inform(models.Model):
    """Inform."""

    class IssueCategory(models.TextChoices):
        HARDWARE = 'HW', 'อุปกรณ์'
        SOFTWARE = 'SW', 'ระบบ'
        OTHER = 'OT', 'อื่น ๆ'

    class InformStatus(models.TextChoices):
        INFORM = 'INF', 'แจ้งซ่อม'
        WAIT = 'WAT', 'รออนุมัติ'
        REJECT = 'REJ', 'ยกเลิก'

    class RepairStatus(models.TextChoices):
        # INFORM = 'INF', 'แจ้งซ่อม'
        # CHECKED = 'CHECKED', 'ตรวจสอบ'
        # WAIT = 'WAT', 'รออนุมัติ'
        ACCEPT = 'ACC', 'ตอบรับ'
        REPAIR = 'RPR', 'ซ่อม'
        COMPLETE = 'CMP', 'ดำเนินการแล้ว'
        REJECT = 'REJ', 'ยกเลิก'
        CLOSE = 'CLO', 'ปิดงาน'
        # WAIT = 'WAT', 'รอวงรอบ'
        # URGENCY = 'URG', 'ซ่อมด่วน'
        # AGENT = 'AGT', 'ซ่อมโดย จนท.ประจำสถานี'

    class ApproveStatus(models.TextChoices):
        APPROVE = 'APR', 'อนุมัติ'
        REJECT = 'RJT', 'ไม่อนุมัติ'
        RECHECK = 'RCK', 'ตรวจสอบใหม่'

    class Urgency(models.TextChoices):
        HIGHT = 'HIG', 'สูงสุด'
        MEDIUM = 'MED', 'ปานกลาง'
        LOW = 'LOW', 'ทั่วไป'

    class RepairCategory(models.TextChoices):
        WAIT = 'WAT', 'วงรอบ'
        URGENCY = 'URG', 'ซ่อมด่วน'
        AGENT = 'AGN', 'ซ่อมโดย จนท.ประจำสถานี'

    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="customer"
    )
    stockitem = models.ForeignKey(
        StockItem,
        on_delete=models.CASCADE,
        related_name="stockitem"
    )
    issue_category = models.CharField(
        max_length=8,
        choices=IssueCategory.choices
    )
    issue = RichTextField()
    urgency = models.CharField(
        max_length=8,
        choices=Urgency.choices,
        default=Urgency.LOW
    )
    inform_status = models.CharField(
        max_length=8,
        choices=InformStatus.choices,
        default=InformStatus.INFORM,
        null=True, blank=True
    )
    approve_status = models.CharField(
        max_length=8,
        choices=ApproveStatus.choices,
        null=True, blank=True
    )
    repair_category = models.CharField(
        max_length=8,
        choices=RepairCategory.choices,
        null=True,
        blank=True
    )
    assigned_to = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    accepted = models.BooleanField(default=False)
    repair_status = models.CharField(
        max_length=8,
        choices=RepairStatus.choices,
        null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)
    closed = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.stockitem.item_name}-{self.created_at}"

    def absolute_url(self):
        return reverse("repair:detail", args=self.pk)


class InformImage(models.Model):
    """ Images Inform """
    inform = models.ForeignKey(
        Inform,
        on_delete=models.CASCADE,
        related_name="inform_image"
    )
    images = models.ImageField(upload_to=inform_image)

    def __str__(self):
        return f"{self.inform.pk} - {self.inform.created_at}"


class InformProgress(models.Model):
    """Progress Inform"""
    inform = models.ForeignKey(
        Inform,
        on_delete=models.CASCADE,
        related_name="inform_progress"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    note = models.TextField(null=True, blank=True)
    status = models.CharField(
        max_length=8,
        choices=Inform.RepairStatus.choices,
        default=Inform.RepairStatus.REPAIR,
        null=True, blank=True
    )

    def __str__(self):
        return f"{self.inform.pk} - {self.inform.created_at}"


# class form reject inform reason
class InformReject(models.Model):
    """Reject Inform"""
    inform = models.ForeignKey(
        Inform,
        on_delete=models.CASCADE,
        related_name="inform_reject"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    reason = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.inform.pk} - {self.inform.created_at}"


class CustomerReview(models.Model):
    """
    Model to represent a Repair Review.

    Attributes:
        date_created (DateTimeField): The date and time the review was created.
        rating (IntegerField): The rating given to the repair service on a scale of 1 to 5.
        description (TextField): A detailed description of the repair experience.
        customer (ForeignKey): The customer who wrote the review.
        inform (ForeignKey): The repair service being reviewed.

    """

    date_created = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    description = models.TextField()
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviewer")
    inform = models.ForeignKey(Inform, on_delete=models.CASCADE, related_name="customer_review")

    class Meta:
        verbose_name = 'Customer Review'
        verbose_name_plural = 'Customer Reviews'

    def __str__(self):
        return f'Repair Review: {self.reviewer} - {self.inform.pk}'


class ManagerReview(models.Model):
    """
    Model to represent a Manager Review.

    Attributes:
        date_created (DateTimeField): The date and time the review was created.
        rating (IntegerField): The rating given to the repair service on a scale of 1 to 5.
        description (TextField): A detailed description of the repair experience.
        manager (ForeignKey): The manager who wrote the review.
        inform (ForeignKey): The repair service being reviewed.

    """

    date_created = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    description = models.TextField()
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    inform = models.ForeignKey(Inform, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Manager Review'
        verbose_name_plural = 'Manager Reviews'

    def __str__(self):
        return f'Manager Review: {self.reviewer} - {self.inform.pk}'


class CommandReview(models.Model):
    """
    Model to represent a Command Review.

    Attributes:
        date_created (DateTimeField): The date and time the review was created.
        rating (IntegerField): The rating given to the repair service on a scale of 1 to 5.
        description (TextField): A detailed description of the repair experience.
        command (ForeignKey): The command who wrote the review.
        inform (ForeignKey): The repair service being reviewed.

    """

    date_created = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    description = models.TextField()
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    inform = models.ForeignKey(Inform, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Command Review'
        verbose_name_plural = 'Command Reviews'

    def __str__(self):
        return f'Command Review: {self.reviewer} - {self.inform.pk}'


# mkae models for manage option for inform : car, job, stockitem
class InformOption(models.Model):
    inform = models.ForeignKey(Inform, on_delete=models.CASCADE)
    car = models.ForeignKey(CarBooking, on_delete=models.CASCADE, null=True, blank=True)
    # job = models.ForeignKey(Job, on_delete=models.CASCADE, null=True, blank=True)
    # stock = models.ForeignKey(Stock, on_delete=models.CASCADE, null=True, blank=True)
