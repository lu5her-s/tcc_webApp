from django.urls import path

from . import views

app_name = "monitor"

urlpatterns = [
    path("", views.MonitorHomeView.as_view(), name="home"),
    path("<int:pk>/", views.MonitorDetailView.as_view(), name="detail"),
]
