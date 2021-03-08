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
        profile_form = ProfileForm()

        if request.method == 'POST':
            user_form = UserCreationForm(request.POST)
            profile_form = ProfileForm(request.POST)
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


def manage_users(request):
    if request.user.is_superuser:
        client_form = ClientForm()
        user_form = UserForm()
        profile_form = ProfileForm()

        context = {
            'user_form': user_form,
            'client_form': client_form,
            'profile_form': profile_form,
        }
        return render(request, 'jobs_engine/manage_users.html', context)
    else:
        return redirect('/')
