#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : urls.py
# Author            : lu5her <lu5her@mail>
# Date              : Thu Sep, 29 2022, 15:34 272
# Last Modified Date: Fri Sep, 30 2022, 11:49 273
# Last Modified By  : lu5her <lu5her@mail>
from django.urls import path

from account import views

app_name = 'account'

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile-update/', views.update_profile, name='profile-update'),
    path('change-password/', views.ChangePassword.as_view(), name='change-password'),

    path('members/', views.MembersListView.as_view(), name='members'),
    path('member/<int:pk>/', views.MembersDetailView.as_view(), name='member'),

    path('sector/<int:pk>/', views.sector_list, name='sector'),
]
