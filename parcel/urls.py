from django.urls import path
from . import views

app_name = 'parcel'

urlpatterns = [
    path('', views.ParcelHomeView.as_view(), name='home'),
    path('bill_list/', views.BillListView.as_view(), name='bill_list'),
    path('bill_detail/<int:pk>/', views.BillDetailView.as_view(), name='bill_detail'),
    path('select_stock/', views.SelectStockView.as_view(), name='select_stock'),
    path('create_bill/<int:pk>/', views.BillCreateView.as_view(), name='create_bill'),
]
