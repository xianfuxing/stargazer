from django.urls import path
from .views import HostDetailView, ItemDetailView, HistoryDetailView, TriggerListView,\
    MonitorListView

app_name = 'monitor'
urlpatterns = [
    path('host/<str:host_name>/', HostDetailView.as_view(), name='host'),
    path('item/<str:host_name>/<str:item_type>/<str:item_key>', ItemDetailView.as_view(), name='item'),
    path('history/<str:host_name>/<str:item_type>/<str:item_key>', HistoryDetailView.as_view(), name='history'),
    path('trigger/', TriggerListView.as_view(), name='trigger'),
    path('', MonitorListView.as_view(), name='list'),
]