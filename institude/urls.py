from django.urls import path
from .views import *

urlpatterns = [
    path('create/',institute_create,name="institute_create")
]
