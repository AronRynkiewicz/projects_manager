from django.shortcuts import render, redirect
from django.http import FileResponse
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
            file.type = 'Client\'s'
            file.file_name = file.file.name
            file.save()
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

    if employee_obj.position.position_name == 'Manager':
        return redirect('accounts:manager_panel')

    if employee_obj.position.position_name == 'Employee':
        return redirect('jobs_engine:tasks_view')


def tasks_view(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    employee_obj = Employee.objects.get(id=request.session.get('employee_id'))
    tasks = Task.objects.filter(assigned_team__in=employee_obj.teams.all())

    context = {
        'tasks': tasks,
    }

    return render(request, 'jobs_engine/employee_view.html', context)


def single_task_view(request, pk):
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    task = Task.objects.get(id=pk)
    file_form = None
    review_form = None
    comment_form = CommentForm()
    comments = task.comments.all().order_by('-creation_date')
    finished_form = None

    try:
        employee_obj = Employee.objects.get(id=request.session.get('employee_id'))
    except Exception:
        employee_obj = None
        finished_form = FinishedForm()

    if employee_obj:
        file_form = FileForm()
        review_form = ReviewForm()

    if request.method == 'POST' and employee_obj:
        file_form = FileForm(request.POST, request.FILES)
        review_form = ReviewForm(request.POST)

        if file_form.is_valid() and review_form.is_valid():
            file = file_form.save()
            file.type = 'Team\'s'
            file.file_name = file.file.name
            file.save()

            task.files.add(file)
            task.save()

            if review_form.cleaned_data['mark_for_review']:
                task.status = 'For client review'
                task.save()
            return redirect('/')

    context = {
        'task': task,
        'file_form': file_form,
        'review_form': review_form,
        'comment_form': comment_form,
        'comments': comments,
        'finished_form': finished_form,
    }
    return render(request, 'jobs_engine/single_task.html', context)


def comment_view(request, pk):
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    task = Task.objects.get(id=pk)
    employee_comment = False

    try:
        Employee.objects.get(id=request.session.get('employee_id'))
        employee_comment = True
    except Exception:
        employee_comment = False

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save()
            if employee_comment:
                task.status = 'For client review'
                comment.type = 'Team\'s'
            else:
                task.status = 'In progress'
                comment.type = 'Client\'s'

            task.save()
            comment.save()
            task.comments.add(comment)
            task.save()
        return redirect('/')


def finished_view(request, pk):
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    task = Task.objects.get(id=pk)
    if request.method == 'POST':
        form = FinishedForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['finished']:
                task.status = 'Finished'
                task.save()

            return redirect('/')


def download(request, pk):
    file = File.objects.get(id=pk)
    filename = file.file.name
    response = FileResponse(open(filename, 'rb'))
    response['Content-Type'] = 'text/plain'
    response['Content-Disposition'] = 'attachment; filename={}'.format(file.file_name)
    return response
