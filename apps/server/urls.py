from django.urls import path
from .views import index, ServerListView, ServerDetailView, DashboardView

app_name = 'server'

urlpatterns = [
    path('list', ServerListView.as_view(), name='list'),
    path('detail/<int:host_id>/', ServerDetailView.as_view(), name='detail'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('fake_bar/', DashboardView, name='fake_bar'),
]
