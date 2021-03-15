from django.urls import path
from . import views

app_name = "permission"

urlpatterns = [
    path('list/', views.PermissionListView.as_view(), name='list'),
    path('create/', views.PermissionCreateView.as_view(), name='create'),
    path('delete/<pk>/', views.PermissionDestroyView.as_view(), name='delete'),
]
