from django.contrib.auth import user_login_failed
from django.dispatch import receiver
from django.core.cache import cache
from axes import attempts


@receiver(user_login_failed)
def on_user_login_failed(sender, credentials, request, **kwargs):
    failures = cache.get(credentials['csrftoken'], 0)
    failures += 1
    cache.set(credentials['csrftoken'], failures, 300)
    print(credentials['csrftoken'], failures)