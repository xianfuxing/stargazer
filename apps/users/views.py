from django.contrib.auth.views import LoginView, LogoutView
from .forms import LoginForm


class MYLoginView(LoginView):
    redirect_authenticated_user = True
    form_class = LoginForm
