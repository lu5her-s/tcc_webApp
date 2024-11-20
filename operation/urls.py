from django.urls import path, include
from . import views

app_name = "operation"

urlpatterns = [
    path("", views.OperationHome.as_view(), name="home"),
    path("create", views.OperationCreateView.as_view(), name="create"),
    path("<int:pk>", views.OperationDetailView.as_view(), name="detail"),
    path("leader/<int:pk>/accept", views.accept_leader, name="accept_leader"),
    path(
        "team/",
        include(
            [
                path(
                    "member/create/<int:pk>",
                    views.team_member_create,
                    name="team_member_create",
                ),
                path(
                    "member/delete/<int:pk>",
                    views.delete_team_member,
                    name="member_delete",
                ),
            ]
        ),
    ),
    # for operation car
    path(
        "car/",
        include(
            [
                path(
                    "add/<int:pk>",
                    views.car_operation_add,
                    name="car_operation_add",
                ),
                path("change/<int:pk>", views.change_car, name="change_car"),
                path("delete/<int:pk>", views.delete_car, name="delete_car"),
            ]
        ),
    ),
    # for operation task
    path(
        "task/",
        include(
            [
                path("add/<int:pk>", views.operation_task_add, name="add_task"),
                path(
                    "delete/<int:pk>",
                    views.operation_task_delete,
                    name="delete_task",
                ),
                path("add_note/<int:pk>", views.operation_note_add, name="add_note"),
            ]
        ),
    ),
    # for oil reimburesment
    path(
        "fuel/",
        include(
            [
                path("add/<int:pk>", views.request_fuel, name="add_fuel"),
                path("update/<int:pk>", views.edit_fuel, name="edit_fuel"),
                path("delete/<int:pk>", views.delete_fuel_request, name="delete_fuel"),
            ]
        ),
    ),
    # for allowance
    path(
        "allowance/",
        include(
            [
                path("add/<int:pk>", views.allowance_add, name="allowance_add"),
                path(
                    "delete/<int:pk>",
                    views.allowance_delete,
                    name="allowance_delete",
                ),
                path(
                    "refund/<int:pk>",
                    views.allowance_refund,
                    name="allowance_refund",
                ),
                path(
                    "refund/update/<int:pk>",
                    views.allowance_refund_update,
                    name="allowance_refund_update",
                ),
                path(
                    "refund/delete/<int:pk>",
                    views.allowance_refund_delete,
                    name="allowance_refund_delete",
                ),
            ]
        ),
    ),
    # for parcel document
    path(
        "parcel/",
        include(
            [
                path(
                    "request/add/<int:pk>",
                    views.parcel_requests_add,
                    name="parcel_request_add",
                ),
                path(
                    "request/delete/<int:pk>",
                    views.parcel_requests_delete,
                    name="parcel_request_delete",
                ),
                path(
                    "return/add/<int:pk>",
                    views.parcel_return_add,
                    name="parcel_return_add",
                ),
                path(
                    "return/delete/<int:pk>",
                    views.parcel_return_delete,
                    name="parcel_return_delete",
                ),
            ]
        ),
    ),
    # for request open/close and approve that
    path(
        "approve/",
        include(
            [
                path("request/open/<int:pk>", views.request_open, name="request_open"),
                path("open/<int:pk>", views.approve_open, name="approve_open"),
                path(
                    "request/close/<int:pk>", views.request_close, name="request_close"
                ),
                path("close/<int:pk>", views.approve_close, name="approve_close"),
            ]
        ),
    ),
    # for inform
    path(
        "inform/",
        include(
            [
                path("add/<int:pk>", views.add_inform, name="add_inform"),
                path("delete/<int:pk>", views.delete_inform, name="delete_inform"),
            ]
        ),
    ),
    path(
        "update_date/<int:pk>",
        views.update_operation_date,
        name="update_date",
    ),
    # operation list for member
    path(
        "member/operation_list",
        views.OperationMemberListView.as_view(),
        name="member_operation_list",
    ),
    # for command
    path(
        "command/",
        include(
            [
                path(
                    "wait/open/",
                    views.OperationCommandWaitOpenListView.as_view(),
                    name="command_wait_open",
                ),
                path(
                    "wait/close/",
                    views.OperationCommandWaitCloseListView.as_view(),
                    name="command_wait_close",
                ),
                path("open/<int:pk>", views.approve_open, name="approve_open"),
                path("close/<int:pk>", views.approve_close, name="approve_close"),
                path(
                    "overview/",
                    views.OperationCommandOverviewListView.as_view(),
                    name="command_overview",
                ),
                path(
                    "overview/stats/",
                    views.OperationOverviewTemplateView.as_view(),
                    name="overview",
                ),
            ]
        ),
    ),
    # for render pdf
    path("operation/<int:pk>/pdf/", views.operation_to_pdf, name="operation_to_pdf"),
]
