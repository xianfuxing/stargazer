from django.urls import path
from .views import index, fake_bar

app_name = 'server'

urlpatterns = [
    path('', index, name='index'),
    path('fake_bar/', fake_bar, name='fake_bar'),
]
