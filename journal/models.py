from account.models import Profile
from django.contrib.auth.models import User
from django.db import models
from django.shortcuts import reverse

# Create your models here.


def get_image_name(instance, filename):
    """get_absolute_url."""
    image_name = instance.journal.title
    return f"JournalImages/%Y/%B/{image_name}/{filename}"


class Journal(models.Model):
    """
    Journal model for journal app

    Attributes:
        author:
        category:
        title:
        body:
        status:
        created_at:
        updated_at:
        header:
    """

    class Status(models.TextChoices):
        IN_PROGRESS = "In Progress", "กำลังทำงาน"
        DONE = "Done", "เสร็จสมบูรณ์"
        CANCELLED = "Cancelled", "ยกเลิก"

    class Category(models.TextChoices):
        ROUTINE = "Routine", "การทำงานตามหน้าที่"
        SPECIAL = "Special", "การทำงานมอบหมาย"
        OTHER = "Other", "การทำงานอื่นๆ"

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(
        max_length=200, choices=Category.choices, default=Category.ROUTINE
    )
    title = models.CharField(max_length=200)
    body = models.TextField()
    status = models.CharField(
        max_length=200, choices=Status.choices, default=Status.IN_PROGRESS
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    header = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="header_journal",
    )

    def __str__(self):
        return f"{self.title} ({self.status})"

    def get_absolute_url(self):
        """get_absolute_url."""
        return reverse("journal:detail", kwargs={"pk": self.pk})


class JournalImage(models.Model):
    """JournalImage."""

    journal = models.ForeignKey(Journal, on_delete=models.CASCADE)
    images = models.ImageField(upload_to="get_image_name", blank=True, null=True)

    class Meta:
        verbose_name = "JournalImage"
        verbose_name_plural = "Images"

    def __str__(self):
        return f"{self.journal.title} by {self.journal.author}"
