import json
import logging
from collections import namedtuple
from django.conf import settings
from celery import task
from aliyunsdkcore import client
from aliyunsdkecs.request.v20140526.DescribeInstancesRequest import DescribeInstancesRequest

from .models import Host


YJH_AK = getattr(settings, 'YJH_AK', '')
YJH_SK = getattr(settings, 'YJH_SK', '')
TBUS_AK = getattr(settings, 'TBUS_AK', '')
TBUS_SK = getattr(settings, 'TBUS_SK', '')
CREDENTIALS = namedtuple('CREDENTIALS', ['AK', 'SK'])
yjh_credentials = CREDENTIALS(YJH_AK, YJH_SK)
tbus_credentials = CREDENTIALS(TBUS_AK, TBUS_SK)


def _send_request(request, clt):
    request.set_accept_format('json')
    try:
        response_str = clt.do_action_with_exception(request)
        logging.info(response_str)
        response_detail = json.loads(response_str)
        return response_detail
    except Exception as e:
        logging.error(e)


@task()
def update_ecs_status():
    resp = {}
    host_list = Host.objects.all()
    request = DescribeInstancesRequest()
    for credential in [yjh_credentials, tbus_credentials]:
        clt = client.AcsClient(credential.AK, credential.SK, 'cn-shenzhen')
        # Get all host from Host model
        for host in host_list:
            request.set_InstanceName(host.hostname)
            response = _send_request(request, clt)
            if response is not None:
                instance_detail = response.get('Instances').get('Instance')[0]
                resp[host.hostname] = instance_detail.get('ExpiredTime')
    return resp
