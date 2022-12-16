from django.urls import path
from . import views

app_name = 'car'

urlpatterns = [
    path('', views.CarListView.as_view(), name='list'),
    path('create/', views.CarCreateView.as_view(), name='create'),
    path('<int:pk>/', views.CarDetailView.as_view(), name='detail'),
    path('update/<int:pk>/', views.CarUpdateView.as_view(), name='update'),
    path('booking/', views.CarBookingListView.as_view(), name='booking'),
    path('booking/create/<int:pk>/', views.CarBookingCreateView.as_view(), name='booking-create'),
    path('booking/detail/<int:pk>/', views.CarBookingDetailView.as_view(), name='booking-detail'),
    path('booking/update/<int:pk>/', views.CarBookingUpdateView.as_view(), name='booking-update'),
    path('booking/wait/', views.WaitApproveListView.as_view(), name='wait_approve'),

    path('return/<int:pk>/', views.ReturnCar, name='return-car'),
    # path('return/<int:pk>/', views.ReturnCar.as_view(), name='return-car'),
    path('use/<int:pk>/', views.UseCar, name='use-car'),
    path('refuel/<int:pk>/', views.RefuelCar, name='refuel'),
    path('fix/create/<int:pk>/', views.CarFixCreateView.as_view(), name='fix-create'),
    path('fix/', views.CarRequestFixListView.as_view(), name='fix'),
    path('fix/<int:pk>/', views.CarRequestFixDetailView.as_view(), name='fix-detail'),
    path('fix/update/<int:pk>/', views.CarFixUpdateView.as_view(), name='fix-update'),
    path('/after-fix/<int:pk>/', views.car_afterfix, name='after-fix'),
]
