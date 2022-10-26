from django.urls import path

from document import views

app_name = 'document'

urlpatterns = [
    path('', views.DocumentHomeView.as_view(), name='home'),
    path('create/', views.DocumentCreateView.as_view(), name='create'),
    path('inbox/', views.InboxListView.as_view(), name='inbox'),
    path('inbox/<int:pk>/', views.InboxDetailView.as_view(), name='inbox-detail'),
    path('outbox/', views.OutboxListView.as_view(), name='outbox'),
    path('outbox/<int:pk>/', views.OutboxDetailView.as_view(), name='outbox-detail'),
    path('accept/<int:pk>/', views.accept_document, name='accept'),
]
