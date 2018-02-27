from django.contrib.auth import user_login_failed
from django.dispatch import receiver
from django.core.cache import cache


@receiver(user_login_failed)
def on_user_login_failed(sender, credentials, request, **kwargs):
    try:
        failures = cache.get(credentials['csrftoken'], 0)
        failures += 1
        cache.set(credentials['csrftoken'], failures, 300)
        print(credentials['csrftoken'], failures)
    except KeyError:
        # 当触发form non filed errors 时候，会先执行这里，才执行LoginView里面的user_login_failed.send
        # 所以就会报KeyError，这里except跳过错误。
        pass
