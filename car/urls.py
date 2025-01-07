from django.urls import include, path

from . import views

app_name = "car"

urlpatterns = [
    path("", views.CarListView.as_view(), name="list"),
    path("create/", views.CarCreateView.as_view(), name="create"),
    path("<int:pk>/", views.CarDetailView.as_view(), name="detail"),
    path("update/<int:pk>/", views.CarUpdateView.as_view(), name="update"),
    path(
        "booking/",
        include(
            [
                path("", views.CarBookingListView.as_view(), name="booking"),
                path(
                    "create/<int:pk>/",
                    views.CarBookingCreateView.as_view(),
                    name="booking-create",
                ),
                path(
                    "detail/<int:pk>/",
                    views.CarBookingDetailView.as_view(),
                    name="booking-detail",
                ),
                path(
                    "update/<int:pk>/",
                    views.CarBookingUpdateView.as_view(),
                    name="booking-update",
                ),
                path("wait/", views.WaitApproveListView.as_view(), name="wait_approve"),
                path(
                    "return/<int:pk>/",
                    views.ReturnCar,
                    name="return-car",
                ),
                path(
                    "approve/<int:pk>/",
                    views.car_booking_approve,
                    name="booking-approve",
                ),
                path(
                    "reject/<int:pk>/",
                    views.car_booking_reject,
                    name="booking-reject",
                ),
                path("use/<int:pk>/", views.UseCar, name="use-car"),
            ]
        ),
    ),
    path(
        "fix/",
        include(
            [
                path("", views.CarRequestFixListView.as_view(), name="fix"),
                path(
                    "create/<int:pk>/",
                    views.CarFixCreateView.as_view(),
                    name="fix-create",
                ),
                path(
                    "<int:pk>/",
                    views.CarRequestFixDetailView.as_view(),
                    name="fix-detail",
                ),
                path(
                    "update/<int:pk>/",
                    views.CarFixUpdateView.as_view(),
                    name="fix-update",
                ),
                path(
                    "after-fix/<int:pk>/",
                    views.CarAfterFixView,
                    name="after-fix",
                ),
                path(
                    "my-fix/",
                    views.ResponsibleListView.as_view(),
                    name="my-fix",
                ),
                path("refuel/<int:pk>/", views.RefuelCar, name="refuel"),
            ]
        ),
    ),
    # path('return/<int:pk>/', views.ReturnCar.as_view(), name='return-car'),
]
