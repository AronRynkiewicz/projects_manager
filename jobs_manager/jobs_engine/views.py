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

    if request.user.is_client:
        return redirect('jobs_engine:client_view')

    if not request.user.is_client:
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
        return redirect('jobs_engine/index.html')


def client_view(request):
    return render(request, 'Client view')


def employee_view(request):
    return render(request, 'Employee view')


def create_credentials(request):
    if request.user.is_superuser:
        form = UserCreationForm()

        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('jobs_engine:create_profile')

        context = {
            'form': form,
        }

        return render(request, 'jobs_engine/create_credentials.html', context)
    else:
        return redirect('jobs_engine/index.html')


def create_profile(request):
    if request.user.is_superuser:
        form = ProfileForm()

        if request.method == 'POST':
            form = ProfileForm(request.POST)
            if form.is_valid():
                profile_obj = form.save()

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
            'form': form,
        }
        return render(request, 'jobs_engine/create_profile.html', context)
    else:
        return redirect('jobs_engine/index.html')


def manage_clients(request):
    if request.user.is_superuser:
        client_form = ClientForm()
        user_form = UserForm()
        profile_form = ProfileForm()

        context = {
            'user_form': user_form,
            'client_form': client_form,
            'profile_form': profile_form,
        }
        return render(request, 'jobs_engine/manage_clients.html', context)
    else:
        return redirect('jobs_engine/index.html')


def manage_employees(request):
    if request.user.is_superuser:
        context = {}
        return render(request, 'jobs_engine/manage_employees.html')
    else:
        return redirect('jobs_engine/index.html')
