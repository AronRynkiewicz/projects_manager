from django import forms
from .models import *


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        exclude = ('assigned_team', 'status', 'files', 'comments',)


class FileForm(forms.ModelForm):
    class Meta:
        model = File
        exclude = ('creation_date', 'type', 'file_name',)


class ReviewForm(forms.Form):
    mark_for_review = forms.BooleanField(initial=False,
                                         label='Mark for Client\'s review?',
                                         required=False,)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ('creation_date', 'type',)


class FinishedForm(forms.Form):
    finished = forms.BooleanField(initial=False,
                                         label='Mark as finished?',
                                         required=False,)
