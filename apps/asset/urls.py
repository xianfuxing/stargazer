from django.urls import path
from .views import AssetOverviewView, SslListView


app_name = 'asset'

urlpatterns = [
    path('', AssetOverviewView.as_view(), name='overview'),
    path('ssl/', SslListView.as_view(), name='ssl')
]