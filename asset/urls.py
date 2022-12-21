from django.urls import path

from asset import views

app_name = 'asset'

urlpatterns = [
    path('', views.AssetHomeView.as_view(), name='stockitem_home'),
    path('list/', views.StockItemListView.as_view(), name='stockitem_list'),
    path('<int:pk>/', views.StockItemDetailView.as_view(), name='stockitem_detail'),
    path('add-item/', views.StockItemCreateView.as_view(), name='stockitem_create'),
]
