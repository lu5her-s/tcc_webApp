#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : urls.py
# Author            : lu5her <lu5her@mail>
# Date              : Thu Sep, 22 2022, 15:06 265
# Last Modified Date: Mon Jun, 24 2024, 16:01 176
# Last Modified By  : lu5her <lu5her@mail>
"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# for test template
from django.views.generic import TemplateView

from account import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("test/", TemplateView.as_view(template_name="test.html"), name="test"),
    path("", views.HomeView.as_view(), name="home"),
    path("contact/", views.ContactView.as_view(), name="contact"),
    # internal url
    path("account/", include("account.urls")),
    path("account/", include("django.contrib.auth.urls")),
    path("announce/", include("announce.urls")),
    path("document/", include("document.urls")),
    path("journal/", include("journal.urls")),
    path("assign/", include("assign.urls")),
    path("car/", include("car.urls")),
    path("asset/", include("asset.urls")),
    path("inform/", include("inform.urls")),
    path("repair/", include("repair.urls")),
    path("parcel/", include("parcel.urls")),
    path("cart/", include("cart.urls")),
    path(
        "operation/",
        include(
            "operation.urls",
        ),
    ),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
    ] + urlpatterns
