from django import forms
from accounts.models import *
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Div, HTML
from crispy_forms.bootstrap import FormActions

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ('user',)


class SignUpForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'email', 'phone', 'sex', 'avatar',)

