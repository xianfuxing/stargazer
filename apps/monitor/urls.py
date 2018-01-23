from django.urls import path
from .views import HostidView


urlpatterns = [
    path('host/<str:host_name>/', HostidView.as_view(), name='hostid'),
]