from django.urls import path
from .views import index, ServerListView

app_name = 'server'

urlpatterns = [
    path('', ServerListView.as_view(), name='list'),
    # path('fake_bar/', fake_bar, name='fake_bar'),
]
