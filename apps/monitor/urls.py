from django.urls import path
from .views import HostidDetailView, ItemDetailView, HistoryDetailView


urlpatterns = [
    path('<str:host_name>/', HostidDetailView.as_view(), name='host'),
    path('<str:host_name>/<str:item_key>', ItemDetailView.as_view(), name='item'),
    path('<str:host_name>/history/<str:item_key>', HistoryDetailView.as_view(), name='history'),
]