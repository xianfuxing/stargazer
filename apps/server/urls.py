from django.urls import path
from .views import index, ServerListView, ServerDetailView, ServerOverviewView

app_name = 'server'

urlpatterns = [
    path('list', ServerListView.as_view(), name='list'),
    path('overview', ServerOverviewView.as_view(), name='overview'),
    path('detail/<int:host_id>/', ServerDetailView.as_view(), name='detail'),
    # path('fake_bar/', DashboardView, name='fake_bar'),
]
