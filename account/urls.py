#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : urls.py
# Author            : lu5her <lu5her@mail>
# Date              : Thu Sep, 29 2022, 15:34 272
# Last Modified Date: Thu Sep, 29 2022, 22:03 272
# Last Modified By  : lu5her <lu5her@mail>
from django.urls import path

from account import views

app_name = 'account'

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile-update/', views.update_profile, name='profile-update'),
]
