from django import forms
from jobs_engine.models import *


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')


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


class TeamForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        members = forms.ModelMultipleChoiceField(
            queryset=Employee.objects.all().exclude(id=kwargs.pop('manager_id', None)),
            widget=forms.CheckboxSelectMultiple,
        )
        super(TeamForm, self).__init__(*args, **kwargs)
        self.fields['members'] = members

    class Meta:
        model = Team
        fields = ('team_name', )
