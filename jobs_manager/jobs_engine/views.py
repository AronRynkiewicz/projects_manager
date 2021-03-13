from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import *


# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    if request.user.is_superuser:
        return redirect('accounts:admin_panel')

    profile_obj = Profile.objects.get(user=request.user)

    if profile_obj.role == 'Client':
        return redirect('jobs_engine:client_view')

    if profile_obj.role == 'Employee':
        return redirect('jobs_engine:employee_view')

    context = {}
    return render(request, 'jobs_engine/index.html', context)


def client_view(request):
    return HttpResponse('Client view')


def employee_view(request):
    employee_obj = Employee.objects.get(profile__user=request.user)
    request.session['employee_id'] = employee_obj.id.__str__()

    if employee_obj.position.position_name == 'Employee':
        return HttpResponse('Employee view')

    if employee_obj.position.position_name == 'Manager':
        return redirect('accounts:manager_panel')
