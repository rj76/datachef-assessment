"""datachef_assessment URL Configuration
"""
from django.urls import path

from apps.banner.views import HomeView


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
]
