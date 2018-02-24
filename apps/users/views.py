from django.shortcuts import redirect, render
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.signals import user_login_failed
from django.core.cache import cache
from .forms import LoginForm, CaptchaLoginForm


class MYLoginView(LoginView):
    redirect_authenticated_user = True
    form_class = LoginForm

    def get(self, request, *args, **kwargs):
        """Handle GET requests: instantiate a blank version of the form."""
        failures = self.get_failures(request)
        if failures >= 3:
            return render(request, 'users/login.html', {'form': CaptchaLoginForm()})
        return self.render_to_response(self.get_context_data())

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            csrftoken = request.COOKIES.get('csrftoken', '')
            user_login_failed.send(
                sender=__name__,
                request=request,
                credentials={
                    'username': form.cleaned_data.get('username'),
                    'csrftoken': csrftoken
                }
            )
            # Check if failed login more than three times
            failures = cache.get(csrftoken, 0)
            if failures >= 3:
                form = CaptchaLoginForm()
            return self.form_invalid(form)

    def get_failures(self, request):
        csrftoken = request.COOKIES.get('csrftoken', '')
        failures = cache.get(csrftoken, 0)
        return failures
