from django.urls import path

from assign import views

app_name = 'assign'

urlpatterns = [
    path('', views.AssignListView.as_view(), name='list'),
    path('staff/', views.AssignStaffListView.as_view(), name='staff-list'),
    path('<int:pk>/', views.AssignDetailView.as_view(), name='detail'),
    path('create/', views.AssignCreateView.as_view(), name='create'),
    path('<int:pk>/update/', views.AssignUpdateView.as_view(), name='update'),
    path('delete/<int:pk>', views.AssignDeleteView.as_view(), name='delete'),

    path('not-accepted/', views.AssignNotAcceptedView.as_view(), name='not-accepted'),

    path('accept/<int:pk>/', views.accepted, name='accept'),
]
