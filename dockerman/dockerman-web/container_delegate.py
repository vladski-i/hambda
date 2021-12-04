import docker
import pprint
import time
from pprint import pprint
import concurrent.futures
from template_delegate import template_file
import json
from bson.objectid import ObjectId
from nginx_delegate import expose_endpoint, prune_conf
from config import get_containers_collection, get_docker_client

executor = concurrent.futures.ThreadPoolExecutor(max_workers = 1)
expose_executor = concurrent.futures.ThreadPoolExecutor(max_workers = 1)
client = get_docker_client()
db = get_containers_collection()

nginx_container = None

nginx_container = tuple(filter(lambda x: x.name == 'nginx', client.containers.list()))
if len(nginx_container) != 1:
    print(f'expected 1 container with name nginx but found {len(nginx_container)}')
nginx_container = nginx_container[0]

TEMPLATES_PATH = './templates'

def _pretty_logs(logs_tee):
    logs = list(logs_tee)
    pretty = []
    for log in logs:
        try:
            pretty.append(log['stream'])
        except KeyError:
            pretty.append(log['aux']['ID'])
    return pretty

def _docker_id_match(first, second):
    l1 = len(first)
    l2 = len(second)
    l = min(l1,l2)
    print(f'comparing {first} and {second} : {first[:l] == second[:l]}')
    return first[:l] == second[:l]

def async_build(tag, id, path, endpoint, code):
    image = None
    logs = None
    tag = tag + str(id)[-4:]
    print(f'attempting build at {path} with tag {tag}')
    try:
        template_file(path, 'app.py', endpoint = endpoint, code = code)
        (image, logs) = client.images.build(path = path, tag = tag, rm = True)
        print('image built')
        try:
            db.containers.update_one({ '_id': id }, { "$set" : {'status' : 'FINISHED', 'logs' : _pretty_logs(logs), 'tag' : tag}} )
        except:
            print('update error')
    except Exception as e:
        print(f'caught {e}')
        containers.update_one({ '_id': id }, { "$set" : {'status' : 'BUILD_FAILED'}} )
        print(f'Build failed for {tag}, {id}')

def _pretty(container):
    return {
        "name" : container.name,
        "id" : container.short_id, 
        "image_tags" : container.image.tags,
        "status" : container.status
        }

def get_containers():
    containers = client.containers.list()
    return tuple(map(lambda x: _pretty(x),containers))

def build_image(tag, id, path, endpoint, code):
    executor.submit(async_build, tag, id, path, endpoint, code)

def async_expose(container_id, endpoint):
    time.sleep(5)
    alive_containers = get_containers()
    print(f"looking for {container_id} in {list(map(lambda x: x['id'], alive_containers))}")
    # if container_id[:l] in map(lambda x: x['id'], alive_containers):
    alive_containers = list(map(lambda x: x['id'], alive_containers))
    print(f'set alive_containers to {alive_containers}')
    alive_containers = list(filter(lambda x: _docker_id_match(x, container_id), alive_containers))
    print(f'set alive_containers to {alive_containers}')
    if len(alive_containers) == 1:
        print(f'exposing container {container_id}')
        expose_endpoint(container_id, endpoint)
        nginx_container.restart()
    else:
        print(f'container {container_id} is dead, skipping exposure')

def run_container(image_id):
    clean()
    img = db.containers.find_one({"_id":ObjectId(image_id)})
    img['_id'] = str(img['_id'])
    tag = img['tag']
    print("tag = " + str(tag)) #PKDBG/Exposure
    container = client.containers.run(tag, detach = True, name = tag, network = "hambda_vlchp")
#    db.containers.update_one({ '_id': id }, { "$set" : {'status' : 'FINISHED', 'logs' : _pretty_logs(logs), 'tag' : tag}} )
    db.containers.update_one({"_id": ObjectId(image_id)}, {"$set" : {'container_id' : container.id[:12]}})    
    print(f"set container_id to {container.id[:10]}")
    expose_executor.submit(async_expose, container.id[:12], img['endpoint'])
    return str(container.logs())

def clean():
    containers = client.containers.list()
    alive_ids = list(map(lambda x:x.short_id,containers))
    prune_conf(alive_ids)
    
def logs(mongo_id=None, container_id=None):
    if not mongo_id and not container_id:
        print("No id passed for logs!")
        return
    if mongo_id:
        img = db.containers.find_one({"_id": ObjectId(mongo_id)})
        print(img)
        container_id = img['container_id']
    containers = client.containers.list()
    containers = list(filter(lambda x: _docker_id_match(x.short_id, container_id), containers))
    print(containers)
    if len(containers) != 1:
        print(f'too few or too many containers found: {containers}')
        return
    container = containers[0]
    # print(f'logs are {str(container.logs())}')
    container_logs = str(container.logs())
    container_logs = container_logs.split('\\n')
    container_logs = container_logs[-min(100, len(container_logs)):]
    return (container_id, container_logs)

if __name__ == "__main__":
    client = docker.from_env()
    pprint.PrettyPrinter().pprint(get_containers(client))