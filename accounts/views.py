from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from rest_framework import serializers, status
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
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Account Created Successfully!")
            return HttpResponseRedirect(reverse('accounts:login'))
    return render(request, 'accounts/signup.html', context={'form': form})




@csrf_exempt #without this get error to show username in toast message box 
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
                messages.success(request, username +" "+"logged in Successfully!")
                # return HttpResponse("logged in yeh")
                return HttpResponseRedirect(reverse('u_dashboard:uhome'))

    return render(request, 'accounts/login.html', context={'form': form})


@login_required
def logout_user(request):
    logout(request)
    messages.info(request, "You are Logged out !")
    # return HttpResponse("logged out yeh")
    return HttpResponseRedirect(reverse('u_dashboard:uhome'))


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





















































from .serializers import RegisterSerializer
from rest_framework.generics import CreateAPIView

class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer