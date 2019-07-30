from django.urls import path
from charaViewer.app_chara.views import (top_view,
                                         login_view,
                                         result_view)

urlpatterns = [
    path('', top_view, name="top"),
    path('login', login_view, name="login"),
    path('result', result_view, name="result"),
]
