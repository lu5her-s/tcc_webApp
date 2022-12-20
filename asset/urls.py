from django.urls import path

from asset import views

app_name = 'asset'

urlpatterns = [
    path('', views.StockItemListView.as_view(), name='list'),
]
