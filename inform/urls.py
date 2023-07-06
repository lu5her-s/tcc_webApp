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

    # technical url
    path('accept/<int:pk>/', views.accept_inform,
         name='accept'),
    path('tech/list/', views.InformTechnicalListView.as_view(),
         name='tech_list'),
    path('tech/progress/', views.InformInProgressListView.as_view(),
         name='tech_progress'),

    # command url
    path('command/approve/<int:pk>/', views.inform_approve,
         name='command_approve'),
]
