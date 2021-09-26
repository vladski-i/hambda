import crossplane
# from container_delegate import exec_container
from functools import lru_cache
from pprint import pprint
import re
import urllib.parse

NGINX_CONF = '/etc/nginx/nginx.conf'
NGINX_DEFAULT_CONF = '/etc/nginx/conf.d/default.conf'

default_conf_json = None
nginx_container = None

def prune_conf(alive_containers):
    server_block = default_conf_json[0]['block']
    locations = list(filter(lambda x: x['directive'] == 'location', server_block))
    non_locations = list(filter(lambda x: x['directive'] != 'location', server_block))
    print(f'locations: {locations}')
    print(f'alive: {alive_containers}')
    new_locations = []
    for location in locations:
        directives = location['block']
        for directive in directives:
            has_proxy = False
            if directive['directive'] == 'proxy_pass':
                has_proxy = True
                print(directive['args'])
                if re.match('http://[a-z0-9]{12}:[0-9]{4}/.*',directive['args'][0]):
                    host = urllib.parse.urlparse(directive['args'][0])
                    if host.netloc[:-7] in alive_containers:
                        new_locations.append(location)
                        break
                else:
                    new_locations.append(location)
                    break
            if not has_proxy:
                new_locations.append(location)
                break
    server_block = non_locations + new_locations
    default_conf_json[0]['block'] = server_block
    print(_build_nginx_conf(default_conf_json))

    with open(NGINX_DEFAULT_CONF, 'w') as f:
        f.write(_build_nginx_conf(default_conf_json))


def _parse_nginx_conf():
    return crossplane.parse(NGINX_CONF)

def _isolate_default(json):
    for file in json['config']:
        if file['file'] == NGINX_DEFAULT_CONF:
            return file['parsed']
    raise ValueError('default.conf not found')

def _build_nginx_conf(json):
    return crossplane.build(json)

def init_nginx_parser():
    global default_conf_json
    conf_json = _parse_nginx_conf()
    default_conf_json = _isolate_default(conf_json)

@lru_cache(maxsize=None)
def nginx_container_id():
    global nginx_container_id
    return nginx_container_id


def restart_nginx():
    print(f"(code,output) : {exec_container(nginx_container_id, '/etc/init.d/nginx restart')}")

def expose_endpoint(host, path):
    global default_conf_json
    if default_conf_json is None:
        raise ValueError('default.conf not loaded')
    server_block = default_conf_json[0]['block']
    server_block.append({
        'directive': 'location',
        'args': [path],
        'block': [ 
            {
            'directive': 'proxy_pass',
            'args': [f'http://{host}:5000{path}'],
            } 
        ]
    })
    default_conf_json[0]['block'] = server_block
    with open(NGINX_DEFAULT_CONF, 'w') as f:
        f.write(_build_nginx_conf(default_conf_json))


if __name__ == "__main__":
    init_nginx_parser()
    expose_endpoint('ghost','/jpath')