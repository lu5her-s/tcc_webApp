#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : models.py
# Author            : lu5her <lu5her@mail>
# Date              : Wed Sep, 28 2022, 22:02 271
# Last Modified Date: Tue Dec, 20 2022, 20:46 354
# Last Modified By  : lu5her <lu5her@mail>
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


def user_directory_path(instance, filename):
    return "user_{0}/{1}".format(instance.user.id, filename)


class Sector(models.Model):
    """This class for create sector for department"""

    name = models.CharField(max_length=200)

    def __str__(self) -> str:
        return f"{self.name}"


class Department(models.Model):
    """
    This class for create department
    ex: name = "มทบ.29", sector="ปก.ทภ.2"
    """

    name = models.CharField(max_length=200)
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.name}"


# NOTE : class for rank
class Rank(models.Model):
    """This class for create rank for user"""

    name = models.CharField(max_length=200)

    def __str__(self) -> str:
        return f"{self.name}"


# NOTE : class for position  ตำแหน่งของ user
class Position(models.Model):
    """for position of user"""

    name = models.CharField(max_length=200)

    def __str__(self) -> str:
        return f"{self.name}"


# NOTE : class for create new profile
class Profile(models.Model):
    """create user profile"""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rank = models.ForeignKey(Rank, on_delete=models.CASCADE, blank=True, null=True)
    position = models.ForeignKey(
        Position, on_delete=models.CASCADE, blank=True, null=True
    )
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE, blank=True, null=True)
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, blank=True, null=True
    )
    place = models.CharField(max_length=200, blank=True, null=True)
    phone = models.CharField(max_length=10, blank=True, null=True)
    image = models.ImageField(upload_to="Profile/", blank=True, null=True)
    about = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    twitter = models.CharField(max_length=200, default="https://twitter.com/#")
    facebook = models.CharField(max_length=200, default="https://facebook.com/#")
    instagram = models.CharField(max_length=200, default="https://instagram.com/#")
    line_id = models.CharField(max_length=200, default="line_id")
    line_token = models.CharField(max_length=200, default="line_token")

    class Meta:
        verbose_name_plural = "Profiles"

    # REVIEW : make return refer
    def __str__(self) -> str:
        if self.rank:
            # return self.rank.name + self.user.get_full_name()
            return f"{self.rank.name} {self.user.get_full_name()}"
        else:
            return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """create_user_profile.
    autocreate when user register

    :param sender:
    :param instance:
    :param created:
    :param kwargs:
    """
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """save_user_profile.
    auto create when user register

    :param sender:
    :param instance:
    :param kwargs:
    """
    instance.profile.save()


# REVIEW: update for token line
class LineToken(models.Model):
    """add Line token for send line notify"""

    name = models.CharField(max_length=200)
    token = models.CharField(max_length=200)
    note = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.name}"
