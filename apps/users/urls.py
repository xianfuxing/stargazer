from django.urls import path
from .views import MYLoginView, LogoutView, ProfileHomeView


app_name = 'users'
urlpatterns = [
    path('login/', MYLoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('profile/', ProfileHomeView.as_view(), name='profile'),
]