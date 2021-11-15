from django.contrib.auth import models
from django.forms import ModelForm
from django import forms
from .models import Institude
class InstituteForm(ModelForm):
    established_date = forms.DateField(
        widget=forms.TextInput(
            attrs={'type': 'date', 'class': 'form-control'}))
    class Meta:
        model= Institude
        exclude= ['owner',]
        # fields = '__all__'