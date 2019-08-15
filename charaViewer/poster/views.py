from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from pychara.exceptions import (PyCharaException,
                                LoginFailureException)
from pychara.session import Session
from charaViewer.poster import APPTITLE
import requests


@require_http_methods(['GET', 'POST'])
def top_view(request):
    context = {'title': APPTITLE,
                'maxItems': range(10)}
    if request.method == 'GET':
        date_api_url = request.build_absolute_uri(reverse('api_date'))
        res = requests.get(date_api_url)
        context['data'] = res.json()['data']
        return render(request, 'poster/top.html', context)
    else:  # POST
        return render(request, 'poster/top.html', context)
