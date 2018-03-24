from django.urls import path
from .views import AssetOverviewView, SslListView, SlsRenewView


app_name = 'asset'

urlpatterns = [
    path('', AssetOverviewView.as_view(), name='overview'),
    path('ssl/', SslListView.as_view(), name='ssl'),
    path('ssl/renew', SlsRenewView.as_view(), name='renew')
]