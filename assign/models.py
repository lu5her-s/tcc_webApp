#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : models.py
# Author            : lu5her <lu5her@mail>
# Date              : Fri Oct, 28 2022, 21:17 301
# Last Modified Date: Fri Oct, 28 2022, 21:40 301
# Last Modified By  : lu5her <lu5her@mail>
from datetime                   import datetime
from django.db                  import models
from django.contrib.auth.models import User
from ckeditor.fields            import RichTextField
from account.models             import Profile

# Create your models here.

def get_image_name(instance, filename):
    file_name = instance.title
    #return 'Assign/{}/{}'.format(file_name, filename)
    return f'Assign/{file_name}/{filename}'


class AssignStatus(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        verbose_name        = 'Status'
        verbose_name_plural = 'Status'

    def __str__(self) -> str:
        """TODO: Docstring for __str__.
        """
        return f"{self.name}"


class Assign(models.Model):
    title       = models.CharField(max_length=200)
    #body        = models.TextField()
    body        = RichTextField()
    author      = models.ForeignKey(User,               on_delete=models.CASCADE, related_name='assignAuthor')
    created_at  = models.DateTimeField(auto_now_add=True)
    assigned_to = models.ForeignKey(Profile,            on_delete=models.CASCADE, related_name='assigned_to')
    accepted    = models.BooleanField(default=False)
    accepted_on = models.DateTimeField('date accepted', null=True,                blank=True)
    status      = models.ForeignKey(AssignStatus,       on_delete=models.CASCADE, related_name='assignStatus', null=True, blank=True)
    note        = RichTextField(null=True,              blank=True)

    def save(self, *args, **kwargs):
        if self.accepted and self.accepted_on is None:
            self.accepted_on = datetime.now()
            self.status      = AssignStatus.objects.get(pk=1)
        elif not self.accepted and self.accepted_on is not None:
            self.accepted_on = None
        super(Assign, self).save(*args, **kwargs)

        def __str__(self):
            # return self.title, self.author.get_full_name(), self.created_at, self.assigned_to.get_full_name(),
            return f"{self.title} to {self.assigned_to.get_full_name()} on {self.created_at.strftime('%a, %d %b %Y %H:%M')}"

class AssignImage(models.Model):
    assign = models.ForeignKey(Assign, on_delete=models.CASCADE)
    images = models.ImageField(upload_to=get_image_name, null=True, blank=True)

    class Meta:
        verbose_name        = 'Images'
        verbose_name_plural = 'Images'

    def __str__(self):
        return f"{self.assign.title}"

class AssignProgress(models.Model):

    """For Update Assign Progress"""
    assign     = models.ForeignKey(Assign,       on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    note       = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name        = "Progress"
        verbose_name_plural = "Progress"

    def __str__(self):
        return f"{self.assign.title} on {self.created_at.strftime('%a, %d %b %Y %H:%M')}"
