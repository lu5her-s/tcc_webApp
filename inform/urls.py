from django.urls import path
from . import views

app_name = 'inform'

urlpatterns = [
    # user url
    path('', views.InformHomeView.as_view(), name="home"),
    path('user/list/', views.InformUserListView.as_view(),
         name="user_list"),
    path('department/list/', views.InformDepartmentListView.as_view(),
         name="department_list"),
    path('agent/list/', views.InformAgentListView.as_view(),
         name="agent_list"),
    path('wait/list/', views.InformWaitListView.as_view(),
         name="wait_list"),
    path('create/', views.InformCreateView.as_view(),
         name="create"),
    path('<int:pk>/', views.InformDetailView.as_view(),
         name="detail"),

    # manager url
    path('manager_list/', views.InformManagerListView.as_view(),
         name='manager_list'),

]
