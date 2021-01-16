from django.urls import path
from . import views

app_name = "deploy"

urlpatterns = [
    path('deploy/', views.DeployView.as_view(), name='deploy'),
]
