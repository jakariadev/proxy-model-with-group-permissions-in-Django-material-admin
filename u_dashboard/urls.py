# pages/urls.py
from django.urls import path
from .views import *
app_name ="u_dashboard"
urlpatterns = [
    path('',dashboard, name='uhome'),
    path('groups/<int:id>/',groups_list, name='groups_list'),
    path('create_user/<int:id>/',create_user, name='create_user'),
    path('add_user/<int:id>/',add_user, name='add_user'),
]
