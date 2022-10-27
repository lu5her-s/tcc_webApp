from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.shortcuts import reverse
from account.models import Profile

# Create your models here.


def get_image_name(instance, filename):
    """get_absolute_url."""
    image_name = instance.journal.title
    return f"JournalImages/%Y/%B/{image_name}/{filename}"


class JournalType(models.Model):
    """JournalType."""

    name = models.CharField(max_length=200)

    def __str__(self):
        """__str__."""
        return f"{self.name}"


class JournalStatus(models.Model):
    """JournalStatus."""

    name = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.name}"


class Journal(models.Model):
    """Journal."""

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(JournalType, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    body = RichTextField()
    status = models.ForeignKey(JournalStatus, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    header = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True, related_name='header_journal')

    def __str__(self):
        return f"{self.title} ({self.status})"

    def get_absolute_url(self):
        """get_absolute_url."""
        return reverse('journal:detail', kwargs={'pk': self.pk})


class JournalImage(models.Model):
    """JournalImage."""

    journal = models.ForeignKey(Journal, on_delete=models.CASCADE)
    images = models.ImageField(upload_to='get_image_name', blank=True, null=True)

    class Meta:
        verbose_name = "JournalImage"
        verbose_name_plural = "Images"

    def __str__(self):
        return f"{self.journal.title} by {self.journal.author}"
