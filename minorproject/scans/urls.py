from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('classify/', views.classify_scan, name='classify'),
    path('history/', views.scan_history, name='history'),
    path("compress/", views.compress_and_save, name="compress_and_save"),
    path("compress/", views.compress_and_save, name="compress_and_save"),
    path("delete/<int:scan_id>/", views.delete_scan, name="delete_scan"),

]
