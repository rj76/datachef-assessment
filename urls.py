"""datachef_assessment URL Configuration
"""
import debug_toolbar
from django.urls import path, include

from apps.banner import views


urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('campaign/<int:pk>/', views.CampaignDetail.as_view(), name='campaign'),
    path('__debug__/', include(debug_toolbar.urls)),
]
