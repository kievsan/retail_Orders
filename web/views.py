import datetime
import os
from pprint import pprint

from django.http import HttpResponse
from django.shortcuts import render, reverse


def home_view(request):
    template_name = 'web/home.html'
    pages = {
        'Главная страница': reverse('home'),
        'Показать текущее время': reverse('time'),
        'Показать содержимое рабочей директории': reverse('workdir')
    }
    context = {
        'pages': pages
    }
    return render(request, template_name, context)


def time_view(request):
    current_time = datetime.datetime.now().time()
    msg = f'Текущее время: {current_time}'
    return HttpResponse(msg)


def workdir_view(request):
    # возвращает список файлов в рабочей директории
    template_name = 'web/workdir.html'
    work_list = os.listdir(os.getcwd())
    pprint(work_list)
    return render(request, template_name, context={'work_list': work_list})
