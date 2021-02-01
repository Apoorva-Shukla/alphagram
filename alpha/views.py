from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.core import serializers
from profile_page.models import Profile

def home(request):
    if request.user.is_authenticated:
        return render(request, 'home.html')

    return render(request, 'log_in.html')

def log_in(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            if request.POST.get('next', ''):
                return redirect(f"{request.POST.get('next', '')}")
            return redirect(f"/{username}/")
        else:
            messages.error(request, 'Either the username or password is wrong! Note that your password and username are case sensitive')
            return redirect(f'{request.path}?next={request.POST.get("next", "")}')

    return render(request, 'log_in.html')

def sign_up(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        if 'sign_up' in request.POST:
            first_name = request.POST.get('first_name', '')
            last_name = request.POST.get('last_name', '')
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            date = int(request.POST.get('date', ''))
            month = request.POST.get('month', '')
            year = int(request.POST.get('year', ''))

            user = User.objects.create_user(username=username, password=password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            profile = Profile(birth_date=date, birth_month=month, birth_year=year, user=user)
            profile.save()

            if request.POST.get('next', ''):
                return redirect(f"{request.POST.get('next', '')}")
            return redirect(f'/{user.username}/')

        if request.POST.get('name', '') == 'username_unique_check':
            username = request.POST.get('username', '')
            username_check = User.objects.filter(username=username).count()

            return JsonResponse(data={
                'username_check': username_check,
            })

        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

    return render(request, 'sign_up.html')

def log_out(request):
    logout(request)

    return redirect('/')