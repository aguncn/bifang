from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.ReleaseListView.as_view(), name='list'),
    path('build/', views.ReleaseBuildView.as_view(), name='build'),
    path('build_status/', views.ReleaseBuildStatusView.as_view(), name='build_status'),
]
