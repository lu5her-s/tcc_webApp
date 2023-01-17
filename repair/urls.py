from django.urls import path
from . import views

app_name = 'repair'

urlpatterns = [
    path('', views.RepairHome.as_view(), name='home'),
    path('inform/', views.InformListView.as_view(), name='inform'),
]
