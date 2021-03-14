from django import forms
from .models import *


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        exclude = ('assigned_team', 'status', 'files')


class FileForm(forms.ModelForm):
    class Meta:
        model = File
        exclude = ('creation_date', 'type')
