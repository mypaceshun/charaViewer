from django.urls import path
from charaViewer.viewer.views import (top_view,
                                      login_view)

urlpatterns = [
    path('', top_view, name="viewer_top"),
    path('login', login_view, name="viewer_login"),
]
