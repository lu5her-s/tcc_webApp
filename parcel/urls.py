from django.urls import path
from . import views

app_name = 'parcel'

urlpatterns = [
    path('', views.ParcelHomeView.as_view(), name='home'),
    path('bill_list/', views.BillListView.as_view(), name='bill_list'),
    path('bill_detail/<int:pk>/', views.BillDetailView.as_view(), name='bill_detail'),
    path('select_stock/', views.SelectStockView.as_view(), name='select_stock'),
    path('select_item/<int:pk>/', views.SelecItemView.as_view(), name='select_item'),
    path('test_create_bill/', views.test_create_bill, name='test_create_bill'),
    path('bill_create/', views.BillCreateView.as_view(), name='bill_create'),
    path('parcel_list/', views.parcel_list, name='parcel_list'),

    path('recieve_item/<int:pk>/', views.recieve_items, name='recieve_item'),
    path('paid_item/<int:pk>/', views.paid_item, name='paid_item'),
    path('approve_request/<int:pk>/', views.approve_request, name='approve_request'),

    path('bill_to_pdf/<int:pk>/', views.bill_to_pdf, name='bill_to_pdf'),
]
