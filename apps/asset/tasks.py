import socket
import ssl
import datetime
from celery import task
from dateutil import parser
from .models import SslCertificate


def get_ssl_info(hostname):
    ssl_date_fmt = r'%b %d %H:%M:%S %Y %Z'

    context = ssl.create_default_context()
    conn = context.wrap_socket(
        socket.socket(socket.AF_INET),
        server_hostname=hostname,
    )
    # 3 second timeout because Lambda has runtime limitations
    conn.settimeout(3.0)

    conn.connect((hostname, 443))
    ssl_info = conn.getpeercert()
    issuer = [i[0] for i in ssl_info.get('issuer', '')]
    issuer_d = {x:y for x, y in issuer}

    # parse the string from the certificate into a Python datetime object
    # expiry_date = datetime.datetime.strptime(ssl_info['notAfter'], ssl_date_fmt)
    expiry_date = parser.parse(ssl_info['notAfter'])
    ssl_type = issuer_d['commonName']
    ssl_provider = issuer_d['organizationName']
    return expiry_date, ssl_provider, ssl_type


@task()
def update_ssl_info():
    status = {}
    hostname_list = SslCertificate.objects.all()
    for hostname in hostname_list:
        expiry_date, ssl_provider, ssl_type = get_ssl_info(hostname.domain)
        hostname.expiry_date = expiry_date
        hostname.issuer = ssl_provider
        hostname.cert_type = ssl_type

        hostname.save()
        status[hostname.domain] = True
    return status

