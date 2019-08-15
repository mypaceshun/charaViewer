from django.urls import path
from charaViewer.api.views import (date_view,
                                   date_items_view)

urlpatterns = [
    path('date', date_view, name="api_date"),
    path('date/<int:value>', date_items_view, name="api_date_items"),
]
