from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import *
from .models import *


# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    if request.user.is_superuser:
        return redirect('jobs_engine:admin_panel')

    profile_obj = Profile.objects.get(user=request.user)

    if profile_obj.role == 'Client':
        return redirect('jobs_engine:client_view')

    if profile_obj.role == 'Employee':
        return redirect('jobs_engine:employee_view')

    context = {}
    return render(request, 'jobs_engine/index.html', context)


def admin_panel(request):
    if request.user.is_superuser:
        context = {
            'clients': Client.objects.all(),
            'employees': Employee.objects.all(),
        }
        return render(request, 'jobs_engine/admin_panel.html', context)
    else:
        return redirect('/')


def client_view(request):
    return HttpResponse('Client view')


def employee_view(request):
    return HttpResponse('Employee view')


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
        return render(request, 'jobs_engine/create_user.html', context)
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
        return render(request, 'jobs_engine/update_user.html', context)
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
        return render(request, 'jobs_engine/delete_user.html', context)
    else:
        return redirect('/')
