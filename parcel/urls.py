#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : urls.py
# Author            : lu5her <lu5her@mail>
# Date              : Sat Jun, 15 2024, 21:48 167
# Last Modified Date: Thu Jun, 20 2024, 17:25 172
# Last Modified By  : lu5her <lu5her@mail>
# -----
from django.urls import path
from . import views

app_name = "parcel"

urlpatterns = [
    path("", views.ParcelHomeView.as_view(), name="home"),
    path("bill_list/", views.BillListView.as_view(), name="bill_list"),
    path("bill_detail/<int:pk>/", views.BillDetailView.as_view(), name="bill_detail"),
    path("select_stock/", views.SelectStockView.as_view(), name="select_stock"),
    path("select_item/<int:pk>/", views.SelecItemView.as_view(), name="select_item"),
    # path('test_create_bill/', views.test_create_bill, name='test_create_bill'),
    path("bill_create/", views.BillCreateView.as_view(), name="bill_create"),
    path("parcel_list/", views.ParcelListView.as_view(), name="parcel_list"),
    path("bill/save_draft/<int:pk>/", views.save_draft, name="save_draft"),
    path("bill/request_bill/<int:pk>/", views.request_bill, name="request_bill"),
    path(
        "item_on_hand_list/",
        views.ItemOnHandListView.as_view(),
        name="item_on_hand_list",
    ),
    # user after request_bill
    path(
        "recieve_item/<int:pk>/", views.RecieveItemsView.as_view(), name="recieve_item"
    ),
    path(
        "parcel_detail/<int:pk>/",
        views.ParcelDetailView.as_view(),
        name="parcel_detail",
    ),
    path("set_item/", views.SetItemLocationView.as_view(), name="set_item"),
    path("replace_item/", views.ReplaceItemLocationView.as_view(), name="replace_item"),
    path(
        "return_parcel/create",
        views.ReturnParcelCreateView.as_view(),
        name="return_parcel_create",
    ),
    path("draft_list/", views.ParcelReturnDraftListView.as_view(), name="draft_list"),
    path(
        "location_list/",
        views.LocationListView.as_view(),
        name="location_list",
    ),
    path(
        "item_on_location/<int:pk>/",
        views.ItemOnLocationView.as_view(),
        name="item_on_location",
    ),
    path("remove_item/", views.RemoveItemView.as_view(), name="remove_item"),
    # return parcel urls
    path(
        "return_parcel/list/",
        views.ParcelReturnListView.as_view(),
        name="return_parcel_list",
    ),
    path(
        "return_parcel/<int:pk>/",
        views.ReturnParcelDetailView.as_view(),
        name="return_parcel_detail",
    ),
    path(
        "return_parcel/save_return_draft/<int:pk>/",
        views.save_return_draft,
        name="save_return_draft",
    ),
    path("return_parcel/return_item/<int:pk>/", views.return_item, name="return_item"),
    # manager ulrs
    path("manager/list/", views.BillManagerListView.as_view(), name="manager_list"),
    path(
        "manager/wait_approve/",
        views.BillWaitApproveListView.as_view(),
        name="manager_wait_approve",
    ),
    path(
        "manager/wait_paid/",
        views.BillWaitPaidListView.as_view(),
        name="manager_wait_paid",
    ),
    path(
        "manager/all_bills/",
        views.ManagerAllBillListView.as_view(),
        name="manager_all_bills",
    ),
    path(
        "manager/request_approve/<int:pk>/",
        views.request_approve,
        name="request_approve",
    ),
    path("set_serial_item/<int:pk>/", views.set_serial_item, name="set_serial_item"),
    path("paid_item/<int:pk>/", views.PaidItemView.as_view(), name="paid_item"),
    path(
        "parcel/return_manager/list/",
        views.ReturnManagerListView.as_view(),
        name="return_manager_list",
    ),
    path(
        "parcel/checker_confirm_return/<int:pk>/",
        views.checker_confirm_return,
        name="checker_confirm_return",
    ),
    # command urls
    # path('approve_request/<int:pk>/', views.approve_request, name='approve_request'),
    path("approve_bill/<int:pk>/", views.approve_bill, name="approve_bill"),
    path(
        "command_wait_approve/list/",
        views.CommandWaitApproveListView.as_view(),
        name="command_wait_approve",
    ),
    path(
        "return_wait_approve/list/",
        views.ReturnCommandListView.as_view(),
        name="return_wait_approve",
    ),
    path("reject_bill/<int:pk>/", views.reject_bill, name="reject_bill"),
    path("bill_to_pdf/<int:pk>/", views.bill_to_pdf, name="bill_to_pdf"),
    path(
        "return_parcel/pdf/<int:pk>/",
        views.return_pdf,
        name="return_pdf",
    ),
    path(
        "command/wait_approve/list/",
        views.ReturnCommandListView.as_view(),
        name="return_command_list",
    ),
    path("approve_return/<int:pk>/", views.return_approve, name="return_approve"),
    path("control_return/<int:pk>/", views.return_controler, name="return_controler"),
    path(
        "return_done/<int:pk>/",
        views.return_done,
        name="return_done",
    ),
]
