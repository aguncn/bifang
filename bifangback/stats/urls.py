from django.urls import path
from . import views

app_name = "stats"

urlpatterns = [
    path('all_count/', views.all_count, name='all_count'),
    path('release_top5/', views.release_top5, name='release_top5'),
    path('release_failed_top5/', views.release_failed_top5, name='release_failed_top5'),
]
