from django.urls import path
from . import views

app_name = "permission"

urlpatterns = [
    path('list/', views.PermissionListView.as_view(), name='list'),
]
