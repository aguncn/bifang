from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.ReleaseListView.as_view(), name='list'),
]
