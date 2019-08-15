from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from pychara.exceptions import (PyCharaException,
                                LoginFailureException)
from pychara.session import Session
from charaViewer.poster import APPTITLE


@require_http_methods(['GET', 'POST'])
def top_view(request):
    context = {'title': APPTITLE}
    if request.method == 'GET':
        return render(request, 'poster/top.html', context)
    else:  # POST
        return render(request, 'poster/top.html', context)
