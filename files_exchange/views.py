from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.core.paginator import Paginator, EmptyPage
from datetime import datetime
from django.utils import timezone
from files_exchange.models import *
from files_exchange.forms import *
# from accounts.models import Profil
from random import *
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required
from django.http import JsonResponse
from django.db.models import Q
from math import *
from django.utils.translation import ugettext as _
from django.utils.translation import ungettext
from django.utils import translation

def test_i18n(request):
    # translation.activate('fr')
    nb_chats = 1
    couleur = "white"
    chaine = _("Hello the newcomers !")
    ip = _("Your IP is %s") % request.META['REMOTE_ADDR']
    infos = ungettext(
        "… and as far I know, you have %(nb)s %(col)s cat !",
        "… and as far I know, you have %(nb)s %(col)s cats !",
        nb_chats) % {'nb': nb_chats, 'col': _(couleur)}
    # Translators: This message informs the user about how many books he can borrow
    quota = _("3 books")
    langage = request.LANGUAGE_CODE

    return render(request, 'files_exchange/test_i18n.html', locals())

def human_readable_size(size, decimal_places=3):
    for unit in ['B','KiB','MiB','GiB','TiB']:
        if size < 1024.0:
            break
        size /= 1024.0
    return f"{size:.{decimal_places}f}{unit}"

def index(request):
    return redirect(reverse('search_files')+'1/')
    # return HttpResponse("Hello, world. You're at the polls index.")

def propose_school_name(request):
    school_short = request.GET.get('school_short', None)
    schools = School.objects.filter(Q(title__icontains=school_short) | Q(city__contains=school_short))[:5]
    school_names = list()
    for school in schools:
        if school.city:
            school_names.append(school.title+', '+school.city)
        else:
            school_names.append(school.title)
    data = {
        'schools': school_names
    }
    return JsonResponse(data)

def search_files(request, id_page=0):
    if id_page==0:
        return redirect(reverse('search_files')+'1/')

    if request.method == 'POST':
        form = SearchFilesForm(request.POST or None)
        print(form)
        if form.is_valid():
            print('valid')
            # return redirect(reverse('result_files'))
            school = School.objects.filter(title=form.cleaned_data['school'])[0]
            promo = form.cleaned_data['promo']
            subject = form.cleaned_data['subject']
            title = form.cleaned_data['title']
            if not title:
                files = FileHomework.objects.filter(school=school, promo=promo, subject=subject, status=1)
                if len(files) == 0:
                    files = FileHomework.objects.filter(promo=promo, subject=subject, status=1)
            else:
                files = FileHomework.objects.filter(school=school, promo=promo, subject=subject, title__icontains=title, status=1)
                if len(files) == 0:
                    files = FileHomework.objects.filter(school=school, promo=promo, subject=subject, status=1)
                if len(files) == 0:
                    files = FileHomework.objects.filter(title__icontains=title, status=1)
                if len(files) == 0:
                    files = FileHomework.objects.filter(promo=promo, subject=subject, status=1)

            # files = FileHomework.objects.all()

            for file in files:
                nb_bytes = os.path.getsize(file.file_pdf.path)
                file.size = human_readable_size(nb_bytes, decimal_places=1)

            paginator = Paginator(files, 10, orphans=5, allow_empty_first_page=True)
            nb_files = len(files)
            try:
                files = paginator.page(id_page)
            except EmptyPage:
                files = paginator.page(paginator.num_pages)

    else:
        form = SearchFilesForm()

    is_post = request.method == 'POST'
    is_form_valid = form.is_valid()
    return render(request, 'files_exchange/search_files.html', locals())
#
# def result_files(request, page=1):
#     return render(request, 'files_exchange/result_files.html', locals())

def one_file_page(request, id_file, title_file):
    file = get_object_or_404(FileHomework, id=id_file, slug_title=title_file)
    if file.status == 1:
        file.nb_views += 1
        file.save()
        nb_bytes = os.path.getsize(file.file_pdf.path)
        file.size = human_readable_size(nb_bytes, decimal_places=1)
    elif file.status == -1:
        return redirect(reverse('search_files'))
    is_published = file.status == 1
    return render(request, 'files_exchange/one_file_page.html', locals())

@login_required
def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.save(commit=False)
            file.school = School.objects.filter(title=form.cleaned_data['school'])[0]
            file.author = request.user
            if request.user.groups.filter(name='moderators').exists():
                file.status = 1
            file.save()
            return redirect(reverse('profil'))
    else:
        form = UploadFileForm()

    return render(request, 'files_exchange/upload_file.html', locals())

@permission_required('files_exchange.add_moderation')
def moderation_page(request):
    if (request.method == 'POST') and (request.POST.get('opinion')):
        mode = Moderation.objects.filter(author=request.user, is_suitable__isnull=True).order_by('-date')[0]
        opinion = request.POST.get('opinion')
        print(opinion)
        mode.is_suitable = opinion
        mode.save()
        if Moderation.objects.filter(filehomework=mode.filehomework, is_suitable=True).count() >= 2:
            file = mode.filehomework
            file.status = 1
            file.save()
        elif Moderation.objects.filter(filehomework=mode.filehomework, is_suitable=False).count() >= 2:
            file = mode.filehomework
            file.status = -1
            file.save()
        return redirect(reverse('moderation_page'))
    else:
        files = FileHomework.objects.filter(status=0).exclude(author=request.user).exclude(moderation__author=request.user).order_by('date')
        if files.count() > 0:
            file = files[0]
        else:
            return redirect(reverse('search_files'))
        mode = Moderation.objects.create(author=request.user, filehomework=file)
    nb_bytes = os.path.getsize(file.file_pdf.path)
    file.size = human_readable_size(nb_bytes, decimal_places=1)
    return render(request, 'files_exchange/moderation_page.html', locals())
