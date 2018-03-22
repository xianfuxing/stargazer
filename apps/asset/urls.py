from django.urls import path
from .views import AssetOverviewView


app_name = 'asset'

urlpatterns = [
    path('', AssetOverviewView.as_view(), name='overview')
]