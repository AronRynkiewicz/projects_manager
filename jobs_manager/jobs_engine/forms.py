from django import forms
from django.forms import ModelForm
from .models import *


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = fields = ('username', 'password')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        exclude = ('task', )


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'
