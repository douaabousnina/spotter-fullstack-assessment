from django.urls import path
from .views import (
    RouteListCreateView,
    RouteRetrieveView,
    LogSheetListCreateView,
    LogSheetRetrieveView
)

urlpatterns = [
    path('routes/', RouteListCreateView.as_view(), name='routes-list-create'),
    path('routes/<uuid:id>/', RouteRetrieveView.as_view(), name='routes-detail'),

    path('logs/', LogSheetListCreateView.as_view(), name='logs-list-create'),
    path('logs/<uuid:id>/', LogSheetRetrieveView.as_view(), name='logs-detail'),
]
