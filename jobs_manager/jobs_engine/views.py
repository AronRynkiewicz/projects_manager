from django.shortcuts import render, redirect
from .forms import *


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
        return render(request, 'jobs_engine/admin_panel.html')
    else:
        return redirect('jobs_engine/index.html')


def client_view(request):
    return render(request, 'Client view')


def employee_view(request):
    return render(request, 'Employee view')


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
