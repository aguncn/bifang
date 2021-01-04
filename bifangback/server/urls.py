from django.urls import path
from . import views

app_name = "server"

urlpatterns = [
    path('list/', views.ServerListView.as_view(), name='list'),
    path('create/', views.ServerCreateView.as_view(), name='create'),
    path('detail/<pk>/', views.ServerRetrieveView.as_view(), name='detail'),
    path('update/<pk>/', views.ServerUpdateView.as_view(), name='update'),
    path('delete/<pk>/', views.ServerDestroyView.as_view(), name='delete'),
]
