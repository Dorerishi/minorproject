from django.urls import path
from .views import classify_scan,home

urlpatterns = [
    path("", home, name="home"),
    path("classify/", classify_scan, name="classify_scan"),
]
