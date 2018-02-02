from django.views.decorators.cache import cache_page


class CacheMixin(object):
    """
    Example from https://gist.github.com/cyberdelia/1231560
    """
    cache_timeout = 60

    def get_cache_timeout(self):
        return self.cache_timeout

    def dispatch(self, *args, **kwargs):
        return cache_page(self.get_cache_timeout())(super(CacheMixin, self).dispatch)(*args, **kwargs)