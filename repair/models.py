from django.db import models
from django.urls import reverse
from account.models import Profile
from django.contrib.auth.models import User
from asset.models import Category, StockItem
from ckeditor.fields import RichTextField

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
        REPAIR = 'RPR', 'ซ่อม'
        COMPLETE = 'CMP', 'แล้วเสร็จ'
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
        WAIT = 'WAT', 'รอวงรอบ'
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
    status = models.CharField(
        max_length=8,
        choices=InformStatus.choices,
        default=InformStatus.INFORM
    )
    approve = models.CharField(
        max_length=8,
        choices=ApproveStatus.choices,
        null=True, blank=True
    )
    category = models.CharField(
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
    created_at = models.DateTimeField(auto_now_add=True)

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


class Repair(models.Model):
    inform = models.ForeignKey(
        Inform,
        on_delete=models.CASCADE,
        related_name='inform_repair'
    )
    operator = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='repair_operator'
    )
    comment = RichTextField(null=True, blank=True)
    cost = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.inform.pk} - {self.inform.status}"