from django.urls import path
from . import views

app_name = 'bill'

urlpatterns = [
    path('', views.BillHomeView.as_view(), name='bill_home'),
    path('list/', views.BillListView.as_view(), name='bill_list'),
    path('select_department/', views.SelectDepartmentView.as_view(), name='select_department'),
    path('request_bill_create/<int:pk>/', views.RequestBillCreateView.as_view(), name='request_bill_create'),
]
