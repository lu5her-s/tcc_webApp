from django.urls import path

from document import views

app_name = 'document'

urlpatterns = [
    path('', views.DocumentHomeView.as_view(), name='home'),
    path('create/', views.DocumentCreateView.as_view(), name='create'),
    path('inbox/', views.InboxListView.as_view(), name='inbox'),
    path('outbox/', views.OutboxListView.as_view(), name='outbox'),
]
