from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('classify/', views.classify_scan, name='classify'),
    path('history/', views.scan_history, name='history'),
]
