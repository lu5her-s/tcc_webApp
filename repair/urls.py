from django.urls import path
from .views import repair_create

app_name = 'repair'

urlpatterns = [
    path('create/', repair_create, name='create'), 
]
