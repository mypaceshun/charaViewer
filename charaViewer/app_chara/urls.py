from django.urls import path
from charaViewer.app_chara.views import (login_view,
                                         result_view)

urlpatterns = [
    path('login', login_view, name="login"),
    path('result', result_view, name="result"),
]
