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
    path('bill/save_draft/<int:pk>/', views.save_draft, name='save_draft'),
    path('bill/request_bill/<int:pk>/', views.request_bill, name='request_bill',),

    # user after request_bill
    path('recieve_item/<int:pk>/', views.recieve_items, name='recieve_item'),
    path('parcel_detail/<int:pk>/', views.parcel_detail, name='parcel_detail',),

    path('set_item_location/<int:pk>/', views.set_item_location, name='set_item_location',),

    # manager ulrs
    path('manager/list/', views.BillManagerListView.as_view(), name='manager_list'),
    path('manager/wait_approve/', views.BillWaitApproveListView.as_view(), name='manager_wait_approve'),
    path('manager/wait_paid/', views.BillWaitPaidListView.as_view(), name='manager_wait_paid'),
    path('manager/all_bills/', views.ManagerAllBillListView.as_view(), name='manager_all_bills'),
    path('manager/request_approve/<int:pk>/', views.request_approve, name='request_approve',),
    path('set_serial_item/<int:pk>/', views.set_serial_item, name='set_serial_item'),
    path('paid_item/<int:pk>/', views.paid_item, name='paid_item'),

    # command urls
    # path('approve_request/<int:pk>/', views.approve_request, name='approve_request'),
    path('approve_bill/<int:pk>/', views.approve_bill, name='approve_bill'),
    path('command_wait_approve/list/', views.CommandWaitApproveListView.as_view(), name='command_wait_approve'),
    path('reject_bill/<int:pk>/', views.reject_bill, name='reject_bill'),

    path('bill_to_pdf/<int:pk>/', views.bill_to_pdf, name='bill_to_pdf'),
]
