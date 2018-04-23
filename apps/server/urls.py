from django.urls import path
from .views import ServerListView, ServerDetailView, ServerOverviewView,\
    ServerSearchView

app_name = 'server'

urlpatterns = [
    path('', ServerListView.as_view(), name='list'),
    path('overview/', ServerOverviewView.as_view(), name='overview'),
    path('detail/<int:host_id>/', ServerDetailView.as_view(), name='detail'),
    path('search/', ServerSearchView.as_view(), name='search'),
]
