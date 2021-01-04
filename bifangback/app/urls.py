from django.urls import path
from . import views

app_name = "app"

urlpatterns = [
    path('list/', views.AppListView.as_view(), name='list'),
    path('create/', views.AppCreateView.as_view(), name='create'),
    path('detail/<pk>/', views.AppRetrieveView.as_view(), name='detail'),
    path('update/<pk>/', views.AppUpdateView.as_view(), name='update'),
    path('delete/<pk>/', views.AppDestroyView.as_view(), name='delete'),
]
