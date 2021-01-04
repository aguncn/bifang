from django.urls import path
from . import views

app_name = "project"

urlpatterns = [
    path('list/', views.ProjectListView.as_view(), name='list'),
    path('create/', views.ProjectCreateView.as_view(), name='create'),
    path('detail/<pk>/', views.ProjectRetrieveView.as_view(), name='detail'),
    path('update/<pk>/', views.ProjectUpdateView.as_view(), name='update'),
    path('delete/<pk>/', views.ProjectDestroyView.as_view(), name='delete'),
]
