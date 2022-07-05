from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .forms import LoginForm

from django.contrib.auth.decorators import login_required

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password']) # authenticate() принимает аргументы request, username и password, и возвращает объект пользователя User, если он успешно аутентифицирован. Впротивном случае вернется None
        if user is not None:
            if user.is_active:
                login(request, user) # Функция login() сохраняет текущего пользователя в сессии
                return HttpResponse('Auth succes')
            else:
                return HttpResponse('Disabled acc')
        else:
            return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


@login_required
def dashboard(request):
    return render(request, 'account/dashboard.html', {'section': 'dashboard'})
