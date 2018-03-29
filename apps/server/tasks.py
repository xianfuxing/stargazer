import json
import logging
from dateutil import parser
from collections import namedtuple
from . import settings_secret
from celery import task
from aliyunsdkcore import client
from aliyunsdkecs.request.v20140526.DescribeInstancesRequest import DescribeInstancesRequest

from .models import Host

YJH_AK = getattr(settings_secret, 'YJH_AK', '')
YJH_SK = getattr(settings_secret, 'YJH_SK', '')
TBUS_AK = getattr(settings_secret, 'TBUS_AK', '')
TBUS_SK = getattr(settings_secret, 'TBUS_SK', '')
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

    # Get all host from Host model
    yjh_clt = client.AcsClient(yjh_credentials.AK, yjh_credentials.SK, 'cn-shenzhen')
    tbus_clt = client.AcsClient(tbus_credentials.AK, tbus_credentials.SK, 'cn-shenzhen')
    for host in host_list:
        clt = yjh_clt if host.org.code == 'YJH' else tbus_clt
        request.set_InstanceName(host.hostname)
        response = _send_request(request, clt)
        if response is not None:
            try:
                instance_detail = response.get('Instances').get('Instance')[0]
                status = instance_detail.get('Status')
                expire_time = instance_detail.get('ExpiredTime')
                resp[host.hostname] = [status, expire_time]
                host.status = status.lower()
                host.expiration_date = parser.parse(expire_time)
                host.save()
            except IndexError:
                raise IndexError('response is empty, please check host and org')
    return resp
