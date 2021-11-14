from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.http import HttpResponse


#Authetication
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate


from accounts.models import *
from accounts.forms import ProfileForm, SignUpForm


#Messages
from django.contrib import messages


from django.contrib.auth import get_user_model
User = get_user_model()


def sign_up(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account Created Successfully!")
            return HttpResponseRedirect(reverse('accounts:login'))
    return render(request, 'accounts/signup.html', context={'form': form})


def login_user(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.warning(request, "logged in Successfully!")
                return HttpResponse("logged in yeh")
                # return HttpResponseRedirect(reverse('institution:home'))

    return render(request, 'accounts/login.html', context={'form': form})


@login_required
def logout_user(request):
    logout(request)
    messages.warning(request, "You are Logged out !")
    return HttpResponse("logged out yeh")
    # return HttpResponseRedirect(reverse('institution:home'))


#profile view

@login_required
def user_profile(request):
    profile = Profile.objects.get(user=request.user)
    form = ProfileForm(instance=profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Change Saved!")
            form = ProfileForm(instance=profile)
    return render(request, 'accounts/change_profile.html', context={'form': form})























































# # for rest api login/ signup
# @api_view(['POST',])
# def registrationAPI(request):
#     username=request.data['username']
#     email=request.data['email']
#     first_name=request.data['first_name']
#     last_name=request.data['last_name']
#     password1=request.data['password1']
#     password2=request.data['password2']
#     phone=request.data.get('phone', None)
#     sex=request.data.get('sex', None)
    
#     if User.objects.filter(username=username).exists():
#         return Response({"error":"An user with that username already exists!"})
#     if password1 != password2:
#         return Response({"error":"Two password didn't matched!"})
    
#     user=User()
#     user.username=username
#     user.email=email
#     user.first_name=first_name
#     user.last_name=last_name
#     if phone:
#         user.phone=phone
#     if sex:
#         user.sex=sex
#     user.is_active=True
#     user.set_password(raw_password=password1)
#     user.save()
    
#     return Response({"Success":"User successfully Registered!"}, status=status.HTTP_201_CREATED)



