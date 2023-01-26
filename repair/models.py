from django.db import models
from account.models import Profile
from django.contrib.auth.models import User
from asset.models import StockItem
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
        HW = 'HARDWARE', 'อุปกรณ์'
        SW = 'SOFTWARE', 'ระบบ'
        OTH = 'OTHER', 'อื่น ๆ'

    class RepairStatus(models.TextChoices):
        INF = 'INFORM', 'แจ้งซ่อม'
        CHK = 'CHECKED', 'ตรวจสอบ'
        REP = 'REPAIR', 'ซ่อม'
        COM = 'COMPLETE', 'แล้วเสร็จ'
        REJ = 'REJECT', 'ยกเลิก'
        WAT = 'WAIT', 'รอวงรอบ'
        URG = 'URGENCY', 'ซ่อมด่วน'
        AGN = 'AGENT', 'ซ่อมโดย จนท.ประจำสถานี'

    class Urgency(models.TextChoices):
        HIG = 'HIGHT', 'สูงสุด'
        MED = 'MEDIUM', 'ปานกลาง'
        LOW = 'LOW', 'ทั่วไป'


    customer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="customer")
    stockitem = models.ForeignKey(
        StockItem, on_delete=models.CASCADE, related_name="stockitem"
    )
    issue_category = models.CharField(max_length=8, choices=IssueCategory.choices)
    issue = RichTextField()
    urgency = models.CharField(
        max_length=8, choices=Urgency.choices, default=Urgency.LOW
    )
    status = models.CharField(
        max_length=8, choices=RepairStatus.choices, default=RepairStatus.INF)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.stockitem.item_name}-{self.created_at}"


class InformImage(models.Model):
    """ Images Inform """
    inform = models.ForeignKey(
        Inform, on_delete=models.CASCADE, related_name="inform_image")
    images = models.ImageField(upload_to=inform_image)

    def __str__(self):
        return f"{self.inform.pk} - {self.inform.created_at}"


class Repair(models.Model):
    inform = models.ForeignKey(
        Inform, on_delete=models.CASCADE, related_name='inform_repair')
    operator = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='repair_operator')
    comment = RichTextField(null=True, blank=True)
    cost = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.inform.pk} - {self.inform.status}"
