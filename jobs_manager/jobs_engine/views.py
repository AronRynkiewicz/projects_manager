from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import *
from .forms import *


# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    if request.user.is_superuser:
        return redirect('accounts:admin_panel')

    profile_obj = Profile.objects.get(user=request.user)

    if profile_obj.role == 'Client':
        client_obj = Client.objects.get(profile__user=request.user)
        request.session['client_id'] = client_obj.id.__str__()
        return redirect('jobs_engine:client_view')

    if profile_obj.role == 'Employee':
        return redirect('jobs_engine:employee_view')

    context = {}
    return render(request, 'jobs_engine/index.html', context)


def client_view(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    client = Client.objects.get(id=request.session.get('client_id'))
    print(Task.objects.all())
    tasks = client.task.all()

    context = {
        'client': client,
        'tasks': tasks,
    }
    return render(request, 'jobs_engine/client_panel.html', context)


def create_task(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    client = Client.objects.get(id=request.session.get('client_id'))
    file_form = FileForm()
    task_form = TaskForm()

    if request.method == 'POST':
        task_form = TaskForm(request.POST)
        file_form = FileForm(request.POST, request.FILES)

        if task_form.is_valid() and file_form.is_valid():
            file = file_form.save()
            task = task_form.save()

            task.files.add(file)
            task.save()

            client.task.add(task)
            client.save()
            return redirect('/')

    context = {
        'task_form': task_form,
        'file_form': file_form,
    }

    return render(request, 'jobs_engine/create_task.html', context)


def employee_view(request):
    employee_obj = Employee.objects.get(profile__user=request.user)
    request.session['employee_id'] = employee_obj.id.__str__()

    if employee_obj.position.position_name == 'Employee':
        return HttpResponse('Employee view')

    if employee_obj.position.position_name == 'Manager':
        return redirect('accounts:manager_panel')
