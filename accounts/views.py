from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.contrib.auth import get_user_model
User = get_user_model()

@api_view(['POST',])
def registrationAPI(request):
    username=request.data['username']
    email=request.data['email']
    first_name=request.data['first_name']
    last_name=request.data['last_name']
    password1=request.data['password1']
    password2=request.data['password2']
    phone=request.data.get('phone', None)
    sex=request.data.get('sex', None)
    
    if User.objects.filter(username=username).exists():
        return Response({"error":"An user with that username already exists!"})
    if password1 != password2:
        return Response({"error":"Two password didn't matched!"})
    
    user=User()
    user.username=username
    user.email=email
    user.first_name=first_name
    user.last_name=last_name
    if phone:
        user.phone=phone
    if sex:
        user.sex=sex
    user.is_active=True
    user.set_password(raw_password=password1)
    user.save()
    
    return Response({"Success":"User successfully Registered!"}, status=status.HTTP_201_CREATED)

