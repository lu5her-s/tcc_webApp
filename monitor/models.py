from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Monitor(models.Model):
    class Status(models.TextChoices):
        NORMAL = "NM", "ปกติ"
        ISSUE = "IS", "ปัญหา"
        PENDING = "PE", "รอดำเนินการ"
        CLOSED = "CL", "ปิดระบบ"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=2, choices=Status.choices, default=Status.NORMAL
    )
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} - {self.status} at {self.created_at}"
