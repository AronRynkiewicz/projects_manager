from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .forms import *


def login_view(request):
    valid = 1
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('jobs_engine:index')
        else:
            valid = 0
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form, 'valid': valid})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('jobs_engine:index')


def admin_panel(request):
    if request.user.is_superuser:
        context = {
            'clients': Client.objects.all(),
            'employees': Employee.objects.all(),
        }
        return render(request, 'accounts/admin_panel.html', context)
    else:
        return redirect('/')


def manager_panel(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    employee_obj = Employee.objects.get(id=request.session.get('employee_id'))

    if employee_obj.position.position_name == 'Manager':
        teams_lst = [team.id.__str__() for team in employee_obj.teams.all()]
        members = Employee.objects.filter(teams__id__in=teams_lst)

        teams = Team.objects.filter(id__in=teams_lst)
        tasks = Task.objects.filter(assigned_team__in=teams_lst)
        available_tasks = Task.objects.filter(assigned_team=None)

        context = {
            'tasks': tasks,
            'teams': teams,
            'members': members,
            'available_tasks': available_tasks,
        }
        return render(request, 'accounts/manager_panel.html', context)

    return redirect('/')


def create_team(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    employee_obj = Employee.objects.get(id=request.session.get('employee_id'))

    if employee_obj.position.position_name == 'Manager':
        form = TeamForm()

        if request.method == 'POST':
            form = TeamForm(request.POST)

            if form.is_valid():
                team = form.save()

                for member in form.cleaned_data['members']:
                    member.teams.add(team)
                    member.save()

                return redirect('/')

        context = {'form': form}

        return render(request, 'accounts/create_team.html', context)

    return redirect('/')


def create_user(request):
    if request.user.is_superuser:
        user_form = UserCreationForm()
        profile_form = ProfileForm(created=True)

        if request.method == 'POST':
            user_form = UserCreationForm(request.POST)
            profile_form = ProfileForm(request.POST, created=True)
            if user_form.is_valid() and profile_form.is_valid():
                user_obj = user_form.save()
                profile_obj = profile_form.save()
                profile_obj.user = user_obj
                profile_obj.save()

                if profile_obj.role == 'Client':
                    obj, created = Client.objects.get_or_create(
                        profile=profile_obj,
                    )
                else:
                    obj, created = Employee.objects.get_or_create(
                        profile=profile_obj,
                        position=Position.objects.get(position_name='Employee')
                    )
                return redirect('/')
        context = {
            'user_form': user_form,
            'profile_form': profile_form,
        }
        return render(request, 'accounts/create_user.html', context)
    else:
        return redirect('/')


def update_user(request, pk):
    if request.user.is_superuser:
        client = Client.objects.filter(id=pk)
        if client:
            role = 'client'
            client = client[0]
            profile_form = ProfileForm(instance=client.profile)
            employee_form = None
        else:
            role = 'employee'
            employee = Employee.objects.get(id=pk)
            profile_form = ProfileForm(instance=employee.profile)
            employee_form = EmployeeForm(instance=employee)

        if request.method == 'POST':
            if role == 'client':
                profile_form = ProfileForm(request.POST, instance=client.profile)
            if role == 'employee':
                profile_form = ProfileForm(request.POST, instance=employee.profile)
                employee_form = EmployeeForm(request.POST, instance=employee)

            if profile_form.is_valid():
                profile_form.save()
                if employee_form:
                    if employee_form.is_valid():
                        employee_form.save()
                        return redirect('/')
                else:
                    return redirect('/')

        context = {
            'form': profile_form,
            'employee_form': employee_form,
        }
        return render(request, 'accounts/update_user.html', context)
    else:
        return redirect('/')


def delete_user(request, pk):
    if request.user.is_superuser:
        client = Client.objects.filter(id=pk)
        if client:
            client = client[0]
            profile_obj = Profile.objects.get(id=client.profile.id)
            user_obj = User.objects.get(id=client.profile.user.id)
            main_obj = client
        else:
            employee = Employee.objects.get(id=pk)
            profile_obj = Profile.objects.get(id=employee.profile.id)
            user_obj = User.objects.get(id=employee.profile.user.id)
            main_obj = employee

        if request.method == 'POST':
            main_obj.delete()
            profile_obj.delete()
            user_obj.delete()
            return redirect('/')

        context = {'profile_obj': profile_obj}
        return render(request, 'accounts/delete_user.html', context)
    else:
        return redirect('/')