from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model

import datetime as dt

from accounts.forms import UserLoginForm, UserRegistrationForm, UserUpdateForm, ContactForm
from scraping_app.models import Error

User = get_user_model()


def login_view(request):
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        data = form.cleaned_data
        email = data.get('email')
        password = data.get('password')
        user = authenticate(request, email=email, password=password)
        login(request, user)
        return redirect('main')
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('main')


def registration_view(request):
    form = UserRegistrationForm(request.POST or None)
    if form.is_valid():
        new_user = form.save(commit=False)
        new_user.set_password(form.cleaned_data['password'])
        new_user.save()
        messages.success(request, 'Пользователь успешно зарегистрирован!')
        return render(request, 'accounts/register_done.html', {'new_user': new_user})

    return render(request, 'accounts/register.html', {'form': form})


def profile_settings(request):
    if request.user.is_authenticated:
        user = request.user
        if request.method == 'POST':
            form = UserUpdateForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                user.city = data['city']
                user.language = data['language']
                user.send_email = data['send_email']
                user.save()
                messages.success(request, 'Настройки обновлены!')
                return redirect('accounts:profile_settings')
        else:
            form = UserUpdateForm(initial={'city': user.city, 'language': user.language, 'send_email': user.send_email})
            return render(request, 'accounts/profile_settings.html', {'form': form})
    else:
        return redirect('accounts:login_view')


def delete_view(request):
    if request.user.is_authenticated:
        user = request.user
        if request.method == 'POST':
            qs = User.objects.get(pk=user.pk)
            qs.delete()
            messages.error(request, 'Пользователь успешно удалён.')
    return redirect('main')


def contact_view(request):
    contact_form = ContactForm()

    errors = []
    if request.user.is_authenticated:
        if request.method == 'POST':
            contact_form = ContactForm(request.POST or None)
            if contact_form.is_valid():
                data = contact_form.cleaned_data
                input_text = data.get('input_area')
                email = data.get('email')
                qs = Error.objects.filter(timestamp=dt.date.today())
                data = [{'input_text': input_text, 'email': email}]
                Error(data=f"user_data:{data}").save()
                messages.success(request, 'Сообщение отправлено')
            else:
                return redirect('accounts/contact.html')
        user = request.user
        return render(request, 'accounts/contact.html', {'form': contact_form})
    else:
        return redirect('accounts:login_view')