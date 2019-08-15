from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods


@require_http_methods(['GET', 'POST'])
def top_view(request):
    return render(request, 'top.html')
