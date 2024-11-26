from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.db import models

# from config.sendline import Sendline

# Create your models here.


def get_image_name(instance, filename):
    image_name = instance.announce.title
    return "Announce/Images/{}/{}".format(image_name, filename)


def get_file_name(instance, filename):
    file_name = instance.announce.title
    return "Announce/Files/{}/{}".format(file_name, filename)


class AnnounceType(models.Model):
    """
    AnnounceType model ประเภทข่าวสาร

    Attributes:
        name:
    """

    name = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.name}"


class AnnounceStatus(models.Model):
    """
    AnnounceStatus model สถานะข่าวสาร

    Attributes:
        name:
    """

    name = models.CharField(max_length=200)

    class Meta:
        verbose_name = "Status"
        verbose_name_plural = "Status"

    def __str__(self):
        return f"{self.name}"


class Announce(models.Model):
    """
    Announce model ข่าวสาร

    Attributes:
        is_type:
        status:
        author:
        title:
        detail:
        created_at:
        updated_at:
        is_delete:
        reads:
    """

    is_type = models.ForeignKey(
        AnnounceType, on_delete=models.CASCADE, related_name="announce_type"
    )
    status = models.ForeignKey(
        AnnounceStatus, on_delete=models.CASCADE, related_name="announce_status"
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    # detail = models.TextField(null=True, blank=True)
    detail = RichTextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_delete = models.BooleanField(default=False)
    reads = models.ManyToManyField(User, related_name="readers", blank=True)

    def __str__(self):
        # return '(' + self.is_type.name + ')' + self.name + '(' + self.author.username + ')' + self.created_at.strftime('%a, %d %b %Y %H:%M:%S') + '--' + str(self.number_of_reader()) + ' reader'
        return f"({self.is_type.name}) {self.title} by {self.author.username}"

    def number_of_reader(self):
        return self.reads.count()


class AnnounceImage(models.Model):
    """
    AnnounceImage model รูปภาพ

    Attributes:
        announce:
        images:
    """

    announce = models.ForeignKey(Announce, on_delete=models.CASCADE)
    images = models.ImageField(upload_to=get_image_name, blank=True, null=True)

    class Meta:
        verbose_name = "Images"
        verbose_name_plural = "Images"

    def __str__(self):
        # return self.announce.name + '(' + self.announce.author.username + ')'
        return f"{self.announce.title} ({self.announce.author.username})"


class AnnounceFile(models.Model):
    """
    AnnounceFile model เอกสาร

    Attributes:
        announce:
        files:
    """

    announce = models.ForeignKey(Announce, on_delete=models.CASCADE)
    files = models.FileField(upload_to=get_file_name, blank=True, null=True)

    class Meta:
        verbose_name = "File"
        verbose_name_plural = "Files"

    def __str__(self):
        # return self.announce.name + '(' + self.announce.author.username + ')'
        return f"{self.announce.title} ({self.announce.author.username})"


class Comment(models.Model):
    """
    Comment model ความคิดเห็น

    Attributes:
        announce:
        author:
        comment:
        created_at:
    """

    announce = models.ForeignKey(Announce, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        # return 'Comment by ' + self.author.username + ' on ' + self.created_at.strftime('%a, %d %b %Y %H:%M')
        return f"Comment by {self.author.username} on {self.created_at.strftime('%a, %d %b %Y %H:%M')}"
