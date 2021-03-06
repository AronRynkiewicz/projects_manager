from django.shortcuts import render, redirect


# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    if request.user.is_superuser:
        return redirect('jobs_engine:admin_panel')

    context = {}
    return render(request, 'jobs_engine/index.html', context)


def admin_panel(request):
    return render(request, 'jobs_engine/admin_panel.html')
