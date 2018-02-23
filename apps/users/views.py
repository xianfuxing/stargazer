from django.contrib.auth.views import LoginView, LogoutView
from .forms import LoginForm


class MYLoginView(LoginView):
    form_class = LoginForm
