# pages/urls.py
from django.urls import path
from .views import *
app_name ="u_dashboard"
urlpatterns = [
    path('', DashboardView.as_view(), name='uhome'),
]
