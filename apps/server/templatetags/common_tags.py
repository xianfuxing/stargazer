from django import template
from django.db.models import Q

from server.models import Host

try:
    # Django 2.0 or later
    from django.core.urlresolvers import reverse
except ImportError:
    # Django 1.x
    from django.urls import reverse

from server.models import Host


register = template.Library()


@register.simple_tag()
def get_server_alert_status(host_id):
    """
    Check host running status.
    :param host_id:
    :return: str
    """
    host = Host.objects.get(id=host_id)
    if host:
        status = host.status
        if status == 'running':
            return 'run-status-running'
        elif status == 'stopped':
            return 'run-status-stopped'
        elif status == 'retired':
            return 'run-status-retired'
        else:
            return ''
    else:
        return ''


@register.simple_tag()
def is_active_reverse(request, args, *urlnames):
    """
    Check if it is active page
    :param request:
    :param args:
    :param urlnames:
    :return: str
    """
    for urlname in urlnames:
        if args:
            args = [args]
        else:
            args =[]
        url = reverse(urlname, args=args)
        if url in request.path:
            if url == '/' and request.path == '/':
                return 'active'
            elif url == '/' and request.path != '/':
                return ''
            return 'active'
        return ''


@register.simple_tag()
def get_not_running():
    not_running_count = Host.objects.filter(~Q(status='running')).count()
    return not_running_count