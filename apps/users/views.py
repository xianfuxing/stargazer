from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.signals import user_login_failed
from django.conf import settings
from django.core.cache import cache
from .forms import LoginForm, CaptchaLoginForm


class MYLoginView(LoginView):
    redirect_authenticated_user = True
    form_class = LoginForm
    login_failures = settings.CAPTCHA_LOGIN_FAILURES

    def get(self, request, *args, **kwargs):
        """Handle GET requests: instantiate a blank version of the form."""
        failures = self.get_failures(request)
        failures = failures + 1 if failures > 0 else failures
        if failures >= self.login_failures:
            return render(request, 'users/login.html', {'form': CaptchaLoginForm()})
        return self.render_to_response(self.get_context_data())

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        # If failures is gt 3, than use captcha form instead.
        form = self.get_form()
        failures = self.get_failures(request)
        failures = failures + 1 if failures > 0 else failures
        if failures >= self.login_failures:
            form = self.get_form(form_class=CaptchaLoginForm)
        if form.is_valid():
            data = {''}
            return self.form_valid(form)
        else:
            csrf_token = request.COOKIES.get('csrftoken', '')
            user_login_failed.send(
                sender=__name__,
                request=request,
                credentials={
                    'csrftoken': csrf_token
                }
            )
            errors = form.errors
            for field in form.fields:
                _field = form.fields[field]
                print(_field.error_messages)
            non_field_errors = form.non_field_errors()
            if non_field_errors:
                resp = JsonResponse({'success': False, 'msg': non_field_errors})
            elif errors and not non_field_errors:
                resp = JsonResponse({'success': False, 'msg': errors})
            return self.form_invalid(form)

    @staticmethod
    def get_failures(request):
        csrftoken = request.COOKIES.get('csrftoken', '')
        failures = cache.get(csrftoken, 0)
        return failures

