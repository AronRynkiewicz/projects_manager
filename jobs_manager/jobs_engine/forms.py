from django import forms
from django.forms import ModelForm
from .models import *


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = fields = ('username', 'password')


class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        created = kwargs.pop('created', False)
        super(ProfileForm, self).__init__(*args, **kwargs)
        if not created:
            self.fields.pop('role')

    class Meta:
        model = Profile
        exclude = ('user', )


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        exclude = ('task', )


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ('position', )
