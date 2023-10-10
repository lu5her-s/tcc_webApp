from django.urls import path
from . import views

app_name = 'parcel'

urlpatterns = [
    path('', views.ParcelHomeView.as_view(), name='home'),
    path('bill_list/', views.BillListView.as_view(), name='bill_list'),
]
