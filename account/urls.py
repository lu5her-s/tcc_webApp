#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : urls.py
# Author            : lu5her <lu5her@mail>
# Date              : Thu Sep, 29 2022, 15:34 272
# Last Modified Date: Fri Dec, 02 2022, 19:27 336
# Last Modified By  : lu5her <lu5her@mail>
from django.urls import path

from account import views

app_name = "account"

urlpatterns = [
    path("register/", views.RegisterView.as_view(), name="register"),
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("profile-update/", views.update_profile, name="profile-update"),
    path("change-password/", views.ChangePassword.as_view(), name="change-password"),
    path("members/", views.MembersListView.as_view(), name="members"),
    path("member/<int:pk>/", views.MembersDetailView.as_view(), name="member"),
    path("sectors/<int:sector_pk>/", views.sector_list, name="sectors"),
    path("positions/<int:position_pk>/", views.position_list, name="positions"),
    # check username
    path("check-username/", views.check_username, name="check-username"),
]
