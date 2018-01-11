from django import template

from server.models import Host


register = template.Library()

@register.simple_tag()
def get_server_alert_status(host_id):
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