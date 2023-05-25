from django.urls import path
from . import views

app_name = 'inform'

urlpatterns = [
    path('', views.InformHomeView.as_view(), name="home"),
    path('create/', views.InformCreateView.as_view(),
         name="create"),
    path('update/<int:pk>/', views.InformUpdateView.as_view(),
         name="update"),

    # user url
    path('user/list/', views.InformUserListView.as_view(),
         name="user_list"),
    path('department/list/', views.InformDepartmentListView.as_view(),
         name="department_list"),
    path('agent/list/', views.InformAgentListView.as_view(),
         name="agent_list"),
    path('wait/list/', views.InformWaitListView.as_view(),
         name="wait_list"),
    path('<int:pk>/', views.InformDetailView.as_view(),
         name="detail"),

    # manager url
    path('manager/list/', views.InformManagerListView.as_view(),
         name='manager_list'),
    path('manager/wait/', views.InformWaitApproveListView.as_view(),
         name='manager_wait'),

]
