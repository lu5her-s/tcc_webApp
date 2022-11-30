from django.urls import path
from . import views

app_name = 'car'

urlpatterns = [
    path('', views.CarListView.as_view(), name='list'),
    path('create/', views.CarCreateView.as_view(), name='create'),
    path('<int:pk>/', views.CarDetailView.as_view(), name='detail'),
    path('booking/', views.CarBookingListView.as_view(), name='booking'),
    path('booking/create/<int:pk>/', views.CarBookingCreateView.as_view(), name='booking-create'),
    path('booking/detail/<int:pk>/', views.CarBookingDetailView.as_view(), name='booking-detail'),
    path('booking/update/<int:pk>/', views.CarBookingUpdateView.as_view(), name='booking-update'),
    path('booking/wait/', views.WaitApproveListView.as_view(), name='wait_approve'),

    path('return/<int:pk>/', views.ReturnCar, name='return-car'),
]
