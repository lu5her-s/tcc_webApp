from django.urls import path

from asset import views

app_name = 'asset'

urlpatterns = [
    path('', views.StockItemHomeView.as_view(), name='stockitem_home'),
    path('list/', views.StockItemListView.as_view(), name='stockitem_list'),
    path('<int:pk>/', views.StockItemDetailView.as_view(), name='stockitem_detail'),
    path('add-item/', views.StockItemCreateView.as_view(), name='stockitem_create'),
    path('update/<int:pk>/', views.StockItemUpdateView.as_view(), name='stockitem_update'),

    path('manager/home/', views.StockManageHomeView.as_view(), name='manager_home'),
    path('manager/list/', views.StockManagerListView.as_view(), name='manager_list'),

    path('category/<int:pk>/', views.categories_list, name='category_list'),
    path('manufacturer/<int:pk>/', views.manufacturer_list,
         name='manufacturer_list'),
    path('network/<int:pk>/', views.network_list, name='network_list'),

    path('department/list/', views.StockDepartmentListView.as_view(), name='department_list'),
]
