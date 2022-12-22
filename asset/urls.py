from django.urls import path

from asset import views

app_name = 'asset'

urlpatterns = [
    path('', views.AssetHomeView.as_view(), name='stockitem_home'),
    path('list/', views.StockItemListView.as_view(), name='stockitem_list'),
    path('<int:pk>/', views.StockItemDetailView.as_view(), name='stockitem_detail'),
    path('add-item/', views.StockItemCreateView.as_view(), name='stockitem_create'),

    path('category/<int:pk>/', views.categories_list, name='category_list'),
    path('manufacturer/<int:pk>/', views.manufacturer_list, name='manufacturer_list'),
    path('network/<int:pk>/', views.network_list, name='network_list'),
]
