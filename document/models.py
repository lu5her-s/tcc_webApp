from django.contrib.auth.models import User
from django.db import models

from account.models import Profile, Sector

# Create your models here.

def get_file_name(instance, filename):
    """get_file_name. for make file prepare for save

    :param instance:
    :param filename:
    """
    receive_no = instance.document.receive_no
    send_from  = instance.document.send_from
    return f"Document/{send_from}/{receive_no}/{filename}"

class Category(models.Model):
    """Category.
    :for set sep document
    """

    name = models.CharField(max_length=200)

    class Meta:
        verbose_name        = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return f"{self.name}"

class Document(models.Model):
    """Document. for set document"""

    URGENCY = [
        ('ปกติ',    'ปกติ'),
        ('ด่วน',    'ด่วน'),
        ('ด่วนมาก', 'ด่วนมาก'),
        ('ด่วนที่สุด', 'ด่วนที่สุด'),
    ]
    TYPE = [
        ('ปฏิบัติ',    'ปฏิบัติ'),
        ('เพื่อทราบ', 'เพื่อทราบ'),
    ]
    STATUS = [
        ('รอการปฏิบัติ',        'รอการปฏิบัติ'),
        ('แผนกรับแล้ว',        'แผนกรับแล้ว'),
        ('จนท.กำลังดำเนินการ', 'จนท.กำลังดำเนินการ'),
        ('ดำเนินการแล้ว',      'ดำเนินการแล้ว'),
        ('เสร็จสิ้น',           'เสร็จสิ้น'),
    ]
    # Document Detail
    recieve_number  = models.CharField(max_length=200)
    doc_sector      = models.CharField(max_length=200, null=True, blank=True)
    doc_number      = models.CharField(max_length=200)
    doc_date        = models.DateField()
    category        = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    urgency         = models.CharField(max_length=200, choices=URGENCY, default='ปกติ')
    title           = models.TextField()
    detail          = models.TextField()
    report_to       = models.CharField(max_length=200, null=True, blank=True)
    operation       = models.CharField(max_length=200, choices=TYPE, default='เพื่อทราบ')
    # status          = models.CharField(max_length=200, choices=STATUS, default='รอการปฏิบัติ')
    file            = models.FileField(upload_to='Document/%Y/%B/%d/')
    author          = models.ForeignKey(User, on_delete=models.CASCADE, related_name='document_author')
    created_at      = models.DateTimeField(auto_now_add=True)
    assigned_sector = models.ManyToManyField(Sector, related_name='assigned_sector')
    # assigned_user   = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="user_operator")

    def __str__(self):
        return f"หนังสือที่ {self.doc_number} ลงวันที่ {self.doc_date} เรื่อง {self.title}"


# TODO : make document, inbox, sector, to_me model
class Department(models.Model):
    """Department.
    for accepted document from header
    """

    document        = models.ForeignKey(Document, on_delete=models.CASCADE)
    # sector = models.ForeignKey(Sector, on_delete=models.CASCADE)
    recieved        = models.BooleanField(default=False)
    reciever        = models.ForeignKey(User, on_delete=models.CASCADE)
    recieved_at     = models.DateTimeField(auto_now_add=True)
    # assigned_user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    note            = models.TextField(null=True, blank=True)

    def __str__(self):
        """__str__."""
        if self.document.author.profile:
            return f"จาก {self.document.author.profile} ที่ {self.document.doc_number} เรื่อง{self.document.title}"
        else:
            return f"{self.document.doc_number} เรื่อง {self.document.title}"


class Operator(models.Model):
    """Operator.
    for user accepted document
    """

    document    = models.ForeignKey(Document, on_delete=models.CASCADE)
    reciever    = models.ForeignKey(Profile, on_delete=models.CASCADE)
    recieved_at = models.DateTimeField(auto_now_add=True)
    note        = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"หนังสือที่ {self.document.doc_no} เรื่อง {self.document.title}"
