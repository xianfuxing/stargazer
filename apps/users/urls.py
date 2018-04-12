from django.urls import path
from .views import MYLoginView, LogoutView, UserProfileView, MyPasswordChangeView,\
    AvatarUpdateView


app_name = 'users'
urlpatterns = [
    path('login/', MYLoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('password_change/', MyPasswordChangeView.as_view(), name='password_change'),
    path('avatar_change/', AvatarUpdateView.as_view(), name='avatar_change')
]