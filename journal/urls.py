from django.urls import path

from journal import views

app_name = "journal"

urlpatterns = [
    path("", views.JournalListView.as_view(), name="list"),
    path("create/", views.JournalCreateView.as_view(), name="create"),
    path("<int:pk>/", views.JournalDetailView.as_view(), name="detail"),
    path("<int:pk>/update", views.JournalUpdateView.as_view(), name="update"),
    path("<int:pk>/delete", views.JournalDeleteView.as_view(), name="delete"),
    path("category/<int:pk>/", views.JournalCategoriesView, name="category"),
    path("status/<int:pk>/", views.JournalStatusView, name="status"),
]
