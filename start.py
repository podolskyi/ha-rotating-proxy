#!/usr/bin/env python

import os
import jinja2

from subprocess import Popen

HA_CONFIG_TMPL_PATH = 'haproxy.cfg.tmpl'
HA_CONFIG_PATH = '/etc/haproxy/haproxy.cfg'
PROXY_PATH = 'proxies.txt'


def render(tpl_path, context):
    """render haconfig from template
    """
    path, filename = os.path.split(tpl_path)
    template = jinja2.Environment(
        loader=jinja2.FileSystemLoader(path or './'), autoescape=True
    ).get_template(filename)
    return template.render(context)


def create_proxy_config(backends):
    """create haproxy config using the data from proxy list
    """
    context = {'backends': backends}
    return render(HA_CONFIG_TMPL_PATH, context)


def preprocess_proxy_list():
    proxies_list = read_proxy_config(PROXY_PATH)
    return proxies_list


def read_proxy_config(file_name):
    proxies = []
    with open(file_name) as data_file:
        for line in data_file.readlines():
            if not line.strip():
                continue
            ip = line.strip().split(":")[0]
            port = line.strip().split(":")[1]
            p = {'ip': ip, "port": port}
            proxies.append(p)
    return proxies


def write_ha_proxy_config(config):
    """write haproxy file to location `HA_CONFIG_PATH`
    """
    with open(HA_CONFIG_PATH, 'w') as file:
        file.write(config)
        file.flush()


backends = preprocess_proxy_list()
ha_config = create_proxy_config(backends)
write_ha_proxy_config(ha_config)

p = Popen(['haproxy -d -f {}'.format(HA_CONFIG_PATH)], shell=True)
try:
    p.wait()
except KeyboardInterrupt:
    print("Stop")
print('done running')
