from django.urls import path

from announce import views

app_name = 'announce'

urlpatterns = [
    path('', views.AnnounceListView.as_view(), name='list'),
    path('<int:pk>/', views.AnnounceDetailView.as_view(), name='detail'),
    path('create/', views.AnnounceCreateView.as_view(), name='create'),
    path('<int:pk>/update/', views.AnnounceUpdateView.as_view(), name='update'),
    path('delete/<int:pk>', views.AnnounceDeleteView.as_view(), name='delete'),

    path('read/<int:pk>', views.AnnounceRead, name='read'),
    path('not-read/', views.AnnounceNotReadView.as_view(), name='not-read'),
]
