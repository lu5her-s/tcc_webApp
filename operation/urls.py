from django.urls import path
from . import views

app_name = "operation"

urlpatterns = [
    path("", views.OperationHome.as_view(), name="home"),
    path("create", views.OperationCreateView.as_view(), name="create"),
    path("<int:pk>", views.OperationDetailView.as_view(), name="detail"),
    path("leader/<int:pk>/accept", views.accept_leader, name="accept_leader"),
    path(
        "team_member_create/<int:pk>",
        views.team_member_create,
        name="team_member_create",
    ),
    path(
        "member/delete/<int:pk>",
        views.delete_team_member,
        name="member_delete",
    ),
    path(
        "update_date/<int:pk>",
        views.update_operation_date,
        name="update_date",
    ),
    path(
        "car_operation_add/<int:pk>",
        views.car_operation_add,
        name="car_operation_add",
    ),
    path("<int:pk>/change_car", views.change_car, name="change_car"),
    # for add task
    path("add_task/<int:pk>", views.operation_task_add, name="add_task"),
    path("delete_task/<int:pk>", views.operation_task_delete, name="delete_task"),
    # operation list for member
    path(
        "member/operation_list",
        views.OperationMemberListView.as_view(),
        name="member_operation_list",
    ),
    path("add_note/<int:pk>", views.operation_note_add, name="add_note"),
    # for oil reimburesment
    path("add_fuel/<int:pk>", views.request_fuel, name="add_fuel"),
    path("update_fuel/<int:pk>", views.edit_fuel, name="edit_fuel"),
    # for allowance
    path("allowance_add/<int:pk>", views.allowance_add, name="allowance_add"),
    path("allowance_delete/<int:pk>", views.allowance_delete, name="allowance_delete"),
]
