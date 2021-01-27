from django.urls import path
from . import views

app_name = "history"

urlpatterns = [
    path('release/', views.ReleaseHistoryListView.as_view(), name='release'),
    path('server/', views.ServerHistoryListView.as_view(), name='server'),

]
