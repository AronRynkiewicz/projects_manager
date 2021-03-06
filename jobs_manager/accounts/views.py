from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout


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