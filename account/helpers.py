#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : helpers.py
# Author            : lu5her <lu5her@mail>
# Date              : Tue May, 27 2025, 13:36 147
# Last Modified Date: Tue May, 27 2025, 21:07 147
# Last Modified By  : lu5her <lu5her@mail>
# -----
from datetime import date, datetime, time

from django.db.models import Q

from announce.models import Announce
from document.models import Depart, Document
from journal.models import Journal


class UserProfileMixin:
    def get_user_profile_context(self):
        user = self.request.user
        context = {
            "user_form": UserForm(instance=user),
            "profile_form": ProfileForm(instance=user.profile),
            "password_form": PasswordChangeForm(user),
        }
        return context


def get_today_range():
    today_min = datetime.combine(date.today(), time.min)
    today_max = datetime.combine(date.today(), time.max)
    return today_min, today_max


def get_inbox_counts(user):
    sector = user.profile.sector
    all_inbox = Document.objects.filter(assigned_sector=sector).count()
    all_department = Depart.objects.filter(reciever__profile__sector=sector).count()
    new_inbox = abs(all_inbox - all_department)
    return all_inbox, all_department, new_inbox


def get_journals(user):
    today_min, today_max = get_today_range()
    sector = user.profile.sector
    today_journals = Journal.objects.filter(
        author__profile__sector=sector, created_at__range=(today_min, today_max)
    )
    return today_journals


def get_not_read_announces(user):
    try:
        return Announce.objects.filter(~Q(author=user) & ~Q(reads__id=user.id))
    except:
        return Announce.objects.none()
