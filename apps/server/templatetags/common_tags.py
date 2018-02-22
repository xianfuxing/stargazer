import requests
import json
from django import template
from django.db.models import Q
from django.core.cache import cache

from server.models import Host

try:
    # Django 2.0 or later
    from django.core.urlresolvers import reverse
except ImportError:
    # Django 1.x
    from django.urls import reverse

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
    root_urls = [reverse('server:list'), '/']
    detail_base = reverse('server:detail', args=[0]).split('0')[0]
    for urlname in urlnames:
        if args:
            args = [args]
        else:
            args =[]
        url = reverse(urlname, args=args)
        if url in request.path:
            if url == reverse('server:list') and request.path.startswith(detail_base):
                return 'active'
            for r_url in root_urls:
                if url == r_url and r_url == request.path:
                    return 'active'
                elif url == r_url and r_url != request.path:
                    return ''
            return 'active'
        return ''


@register.simple_tag()
def get_server_status_count():
    # Get result from cache if exist
    issue_count = cache.get('issue_count')
    if issue_count:
        return issue_count

    status_count = 0
    not_running_count = Host.objects.filter(~Q(status='running')).count()
    for host in Host.objects.all():
        if host.is_expired:
            status_count += 1
        elif host.will_be_expired:
            status_count += 1

    issue_count = not_running_count + status_count
    cache.set('issue_count', issue_count, 600)
    return issue_count


@register.simple_tag()
def get_trigger_count(request):
    trigger_count = cache.get('trigger_count')
    if trigger_count:
        return trigger_count
    trigger_count = 0
    # Get trigger count from zapi
    url = 'http://' + request.META['HTTP_HOST'] + reverse('monitor:trigger')
    try:
        r = requests.get(url)
        trigger_resp = json.loads(r.text)
        for k in trigger_resp:
            trigger_count += len(trigger_resp[k])
    except Exception as e:
        print(e)
    cache.set('trigger_count', trigger_count, 300)
    return trigger_count


@register.filter(name='my_add')
def my_add(value1, value2):
    return value1 + value2
