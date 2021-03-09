from django.urls import path
from . import views

app_name = "gitapp"

urlpatterns = [
    path('list/', views.GitappListView.as_view(), name='list'),
]
