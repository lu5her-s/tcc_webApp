from django.urls import path

from . import views

app_name = "inform"

urlpatterns = [
    path("", views.InformHomeView.as_view(), name="home"),
    path("create/", views.InformCreateView.as_view(), name="create"),
    path("update/<int:pk>/", views.InformUpdateView.as_view(), name="update"),
    path("all_infrom/", views.all_inform, name="all_inform"),
    path("review/<int:pk>/", views.review_save, name="review"),
    path("pdf/<int:pk>/", views.inform_to_pdf, name="pdf"),
    # user url
    path("user/list/", views.InformUserListView.as_view(), name="user_list"),
    path(
        "department/list/",
        views.InformDepartmentListView.as_view(),
        name="department_list",
    ),
    path("agent/list/", views.InformAgentListView.as_view(), name="agent_list"),
    path("wait/list/", views.InformWaitListView.as_view(), name="wait_list"),
    path("<int:pk>/", views.InformDetailView.as_view(), name="detail"),
    path(
        "customer/wait_to_review/",
        views.customer_wait_to_review,
        name="customer_wait_to_review",
    ),
    # manager url
    path("manager/list/", views.InformManagerListView.as_view(), name="manager_list"),
    path(
        "manager/wait/", views.InformWaitApproveListView.as_view(), name="manager_wait"
    ),
    path("manager/close/", views.staff_wait_close, name="manager_close"),
    # technical url
    path("accept/<int:pk>/", views.accept_inform, name="accept"),
    path("tech/list/", views.InformTechnicalListView.as_view(), name="tech_list"),
    path(
        "tech/progress/", views.InformInProgressListView.as_view(), name="tech_progress"
    ),
    path("tech/note/<int:pk>/", views.repair_note, name="tech_note"),
    path("tech/all_assign/", views.all_assigned, name="tech_all_assign"),
    # command url
    path("command/approve/<int:pk>/", views.inform_approve, name="command_approve"),
    path("command/reject/<int:pk>/", views.inform_reject, name="command_reject"),
    path("wait_close_approve/", views.wait_close_approve, name="wait_close_approve"),
    path(
        "command/wait_approve/", views.command_wait_approve, name="command_wait_approve"
    ),
    path("command/progress/", views.all_progress, name="command_progress"),
    path("command/recheck/", views.all_recheck, name="command_recheck"),
    path("command/close_approve/<int:pk>/", views.close_approve, name="close_approve"),
]
