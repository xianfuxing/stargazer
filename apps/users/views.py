from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import login as auth_login, update_session_auth_hash
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.views.generic import TemplateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.signals import user_login_failed
from django.conf import settings
from django.core.cache import cache
from django.template.defaultfilters import filesizeformat
from braces.views import FormValidMessageMixin
from django.urls import reverse_lazy

from .forms import LoginForm, CaptchaLoginForm,\
    ProfileForm, PasswordChangeCustomForm, MugshotForm
from django.contrib.auth import get_user_model
User = get_user_model()


class MYLoginView(LoginView):
    redirect_authenticated_user = True
    form_class = LoginForm
    login_failures = settings.CAPTCHA_LOGIN_FAILURES

    def get(self, request, *args, **kwargs):
        """Handle GET requests: instantiate a blank version of the form."""
        failures = self.get_failures(request)
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
            data = self.form_valid(form)
            return JsonResponse(data)
        else:
            csrf_token = request.COOKIES.get('csrftoken', '')
            user_login_failed.send(
                sender=__name__,
                request=request,
                credentials={
                    'csrftoken': csrf_token
                }
            )
            data = self.get_form_errors(form)
            if failures >= self.login_failures:
                captcha_html = str(form['captcha'])
                data['captcha'] = captcha_html
            return JsonResponse(data)

            # return self.form_invalid(form)

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        auth_login(self.request, form.get_user())
        data = {'success': True, 'msg': 'success'}
        return data

    @staticmethod
    def get_failures(request):
        csrftoken = request.COOKIES.get('csrftoken', '')
        failures = cache.get(csrftoken, 0)
        return failures

    @staticmethod
    def get_form_errors(form):
        data = {}
        field_errors = {}
        errors = form.errors
        non_field_errors = form.non_field_errors()
        if non_field_errors and not errors:
            data = {'success': False, 'non_field_errors': non_field_errors}
        elif errors and not non_field_errors:
            for k in errors:
                field_errors[k] = errors[k]
            data = {'success': False, 'field_errors': field_errors, 'tips': '请修正下面的错误'}
        elif errors and non_field_errors:
            data = {'success': False, 'field_errors': field_errors, 'non_field_errors': non_field_errors}
        return data


class UserProfileView(LoginRequiredMixin, FormValidMessageMixin, UpdateView):
    template_name = 'users/profile_home.html'
    form_valid_message = "个人资料更新成功！"
    form_class = ProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return User.objects.get(pk=self.request.user.pk)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['pass_form'] = PasswordChangeCustomForm(self.request.user)
        return ctx


class MyPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    form_class = PasswordChangeCustomForm
    template_name = 'users/profile_home.html'
    success_url = reverse_lazy('users:profile')

    def get(self, request, *args, **kwargs):
        return JsonResponse({'msg': 'need post method'})

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        form = self.get_form()
        if form.is_valid():
            # return self.form_valid(form)
            self.form_valid(form)
            return JsonResponse({'success': True, 'msg': 'password changed successfully'})
        else:
            field_errors = {}
            errors = form.errors
            for k in errors:
                field_errors[k] = errors[k]
            return JsonResponse({'success': False, 'field_errors': field_errors})

    def get_context_data(self, **kwargs):
        """Insert the form into the context dict."""
        if 'form' in kwargs:
            del kwargs['form']
        kwargs['pass_form'] = self.get_form()
        return super().get_context_data(**kwargs)


class MugshotUpdateView(LoginRequiredMixin, FormValidMessageMixin, UpdateView):
    template_name = 'users/profile_home.html'
    form_valid_message = "头像更新成功！"
    form_class = MugshotForm
    success_url = reverse_lazy('users:profile')

    def get(self, request, *args, **kwargs):
        return JsonResponse({'msg': 'need post method'})

    # def post(self, request, *args, **kwargs):
    #     form = self.get_form()
    #     if form.is_valid():
    #         return self.form_valid(form)
    #     else:
    #         field_errors = {}
    #         errors = form.errors
    #         for k in errors:
    #             field_errors[k] = errors[k]
    #         return JsonResponse({'success': False, 'field_errors': field_errors})

    def get_object(self, queryset=None):
        return User.objects.get(pk=self.request.user.pk)