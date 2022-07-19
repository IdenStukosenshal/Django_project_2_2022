from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def user_login(request):   # Сейчас это не используется
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


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = ProfileEditForm(data=request.POST, files=request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password']) # Вместо сохранения пароля пользователя «как есть», мы используем метод set_password() модели User. Он сохранит пароль в зашифрованном виде

            new_user.save()
            #new_user.refresh_from_db()

            new_profile = Profile.objects.create(user=new_user, photo=request.FILES['photo'])
            new_profile.save()
            # учебнике в этом месте ошибка, https://ru.stackoverflow.com/questions/923667/%D0%A0%D0%B0%D1%81%D1%88%D0%B8%D1%80%D0%B5%D0%BD%D0%BD%D0%B0%D1%8F-%D1%80%D0%B5%D0%B3%D0%B8%D1%81%D1%82%D1%80%D0%B0%D1%86%D0%B8%D1%8F-%D0%BF%D0%BE%D0%BB%D1%8C%D0%B7%D0%BE%D0%B2%D0%B0%D1%82%D0%B5%D0%BB%D0%B5%D0%B9-%D0%B2-django-2-1

            return render(request, 'account/register_done.html', {'new_user': new_user, 'new_profile': new_profile})
    else:
        user_form = UserRegistrationForm()
        profile_form = ProfileEditForm()
    return render(request, 'account/register.html', {'user_form': user_form, 'profile_form': profile_form})


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, "Error updating your profile")
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'account/edit.html', {'user_form': user_form, 'profile_form': profile_form})





"""Список возможных вопросов:
* Зачем иногда создаётся object = None, а иногда нет?
* Уведомление не закрывается (вопрос скорее по HTML)
* не работает ngrok и csrf, из-за чего возможно не работает java script
* не показывает превью при альтернативном добавлении """
