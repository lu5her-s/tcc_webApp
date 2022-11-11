from django.urls import path
from . import views

app_name = 'car'

urlpatterns = [
    path('', views.CarListView.as_view(), name='list'),
    path('create/', views.CarCreateView.as_view(), name='create'),
    path('<int:pk>/', views.CarDetailView.as_view(), name='detail'),
    path('booking/<int:pk>/', views.CarBookingView.as_view(), name='booking'),
]
