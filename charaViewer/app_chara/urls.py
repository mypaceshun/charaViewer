from django.urls import path
from charaViewer.app_chara.views import (top_view)

urlpatterns = [
    path('', top_view),
]
