from django.urls import path

from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('add/<int:category_id>/', views.cart_add, name='cart_add'),
    path('update/<int:category_id>/', views.update_cart, name='update_cart'),
    path('remove/<int:category_id>/', views.cart_remove, name='cart_remove'),
    path('remain/<int:category_id>/', views.remain_in_stock, name='remain_in_stock'),
]
