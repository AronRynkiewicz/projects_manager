from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .forms import *
import json


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
        teams = []
        for id in teams_lst:
            team = Team.objects.filter(id=id)[0]
            employees = Employee.objects.filter(teams__id=id)
            teams.append([
                team,
                employees,
            ])

        tasks = Task.objects.filter(assigned_team__id__in=teams_lst)
        available_tasks = Task.objects.filter(assigned_team=None)

        context = {
            'tasks': tasks,
            'teams': teams,
            'available_tasks': available_tasks,
        }
        return render(request, 'accounts/manager_panel.html', context)

    return redirect('/')


def create_team(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    employee_obj = Employee.objects.get(id=request.session.get('employee_id'))

    if employee_obj.position.position_name == 'Manager':
        form = TeamForm(manager_id=request.session.get('employee_id'))

        if request.method == 'POST':
            form = TeamForm(request.POST, manager_id=request.session.get('employee_id'))

            if form.is_valid():
                team = form.save()

                employee_obj.teams.add(team)
                employee_obj.save()

                for member in form.cleaned_data['members']:
                    member.teams.add(team)
                    member.save()

                return redirect('/')

        context = {'form': form}

        return render(request, 'accounts/create_team.html', context)

    return redirect('/')


def update_team(request, pk):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    employee_obj = Employee.objects.get(id=request.session.get('employee_id'))

    if employee_obj.position.position_name == 'Manager':
        team = Team.objects.get(id=pk)
        form = TeamForm(instance=team, manager_id=request.session.get('employee_id'))

        original_members = Employee.objects.filter(teams__id=team.id)
        members = [member.id.__str__() for member in original_members if member.id != employee_obj.id]
        json_members = json.dumps(members)
        members = set(members)

        if request.method == 'POST':
            form = TeamForm(request.POST, instance=team, manager_id=request.session.get('employee_id'))

            if form.is_valid():
                new_members = set([member.id.__str__() for member in form.cleaned_data['members']])
                added_members = new_members.difference(new_members.intersection(members))
                removed_members = members.difference(members.intersection(new_members))

                for member in form.cleaned_data['members']:
                    if member.id.__str__() in added_members:
                        member.teams.add(team)
                        member.save()
                for member in original_members:
                    if member.id.__str__() in removed_members:
                        member.teams.remove(team)

                return redirect('/')

        context = {
            'form': form,
            'members': json_members,
        }
        return render(request, 'accounts/update_team.html', context)
    return redirect('/')


def delete_team(request, pk):
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    employee_obj = Employee.objects.get(id=request.session.get('employee_id'))

    if employee_obj.position.position_name == 'Manager':
        team = Team.objects.get(id=pk)
        if request.method == 'POST':
            members = Employee.objects.filter(teams__id=team.id)

            for member in members:
                member.teams.remove(team)

            team.delete()

            return redirect('/')

        context = {
            'team': team,
        }
        return render(request, 'accounts/delete_team.html', context)
    return redirect('/')


def add_team(request, pk):
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    employee_obj = Employee.objects.get(id=request.session.get('employee_id'))

    if employee_obj.position.position_name == 'Manager':
        task = Task.objects.get(id=pk)
        teams_lst = [team.id.__str__() for team in employee_obj.teams.all()]
        add_team_form = TeamAdditionForm(teams_id_lst=teams_lst)

        if request.method == 'POST':
            add_team_form = TeamAdditionForm(request.POST, teams_id_lst=teams_lst)
            if add_team_form.is_valid():
                task.status = 'In progress'
                task.save()

                for team in add_team_form.cleaned_data['teams']:
                    task.assigned_team.add(team)
                    task.save()
                return redirect('/')

        context = {
            'task': task,
            'form': add_team_form,
        }
        return render(request, 'accounts/add_team.html', context)
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


def search_user(request):
    if request.user.is_superuser:
        form = SearchUserForm()
        users = set()
        if request.method == 'POST':
            form = SearchUserForm(request.POST)
            if form.is_valid():
                name_or_surname = form.cleaned_data['name_or_surname']
                clients = Client.objects.filter(profile__name__contains=name_or_surname)
                for i in clients:
                    users.add(i)
                clients = Client.objects.filter(profile__surname__contains=name_or_surname)
                for i in clients:
                    users.add(i)

                emps = Employee.objects.filter(profile__name__contains=name_or_surname)
                for i in emps:
                    users.add(i)

                emps = Employee.objects.filter(profile__surname__contains=name_or_surname)
                for i in emps:
                    users.add(i)
        context = {
            'form': form,
            'users': users,
        }
        return render(request, 'accounts/search_user.html', context)
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
