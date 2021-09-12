import crossplane

NGINX_CONF = '/etc/nginx/nginx.conf'
NGINX_DEFAULT_CONF = '/etc/nginx/conf.d/default.conf'

default_conf_json = None

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