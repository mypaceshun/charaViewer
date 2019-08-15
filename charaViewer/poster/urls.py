from django.urls import path
from charaViewer.poster.views import (top_view)

urlpatterns = [
    path('', top_view, name="poster_top"),
]
