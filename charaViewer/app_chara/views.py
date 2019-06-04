from django.shortcuts import render


def top_view(request):
    context = {}
    return render(request, 'base.html', context)
