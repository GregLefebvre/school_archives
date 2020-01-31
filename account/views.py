from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.core.paginator import Paginator, EmptyPage
from datetime import datetime
from django.utils import timezone
from files_exchange.models import *
from files_exchange.forms import *
from account.forms import *
# from accounts.models import Profil
from random import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
from math import *

def human_readable_size(size, decimal_places=3):
    for unit in ['B','KiB','MiB','GiB','TiB']:
        if size < 1024.0:
            break
        size /= 1024.0
    return f"{size:.{decimal_places}f}{unit}"

def log_in(request):
    if request.method == 'POST':
        email = request.POST.get('email', False)
        password = request.POST.get('password', False)
        if User.objects.filter(email=email).exists():
            username = User.objects.filter(email=email)[0].username
        else:
            username = ''
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            return redirect(reverse('search_files'))
            # return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    return render(request, 'account/log_in.html', locals())

def log_out(request):
    logout(request)
    return redirect(reverse('search_files'))

def sign_up(request):
    if request.user.is_authenticated:
        return redirect(reverse('search_files'))

    if request.method == 'POST':
        form = CreateUserForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            # print(username+' '+email+' '+password)
            user = User.objects.create_user(username, email, password)
            user.save()
            login(request, user)
            return redirect(reverse('search_files'))
    else:
        form = CreateUserForm()
    return render(request, 'account/sign_up.html', locals())

def profil(request):
    if request.user.is_authenticated:
        user = request.user
        files = FileHomework.objects.filter(author=user).order_by('-date')
        profil = True
        for file in files:
            nb_bytes = os.path.getsize(file.file_pdf.path)
            file.size = human_readable_size(nb_bytes, decimal_places=1)
        return render(request, 'account/profil.html', locals())
    return redirect(reverse('search_files'))
