import docker
import pprint
from pprint import pprint
import concurrent.futures
from template_delegate import template_file
import json
from bson.objectid import ObjectId
from nginx_delegate import expose_endpoint

executor = concurrent.futures.ThreadPoolExecutor(max_workers = 1)

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


def async_build(client, collection, tag, id, path, endpoint, code):
    image = None
    logs = None
    tag = tag + str(id)
    print(f'attempting build at {path} with tag {tag}')
    try:
        template_file(path, 'app.py', endpoint = endpoint, code = code)
        (image, logs) = client.images.build(path = path, tag = tag, rm = True)
        print('image built')
        try:
            collection.update_one({ '_id': id }, { "$set" : {'status' : 'FINISHED', 'logs' : _pretty_logs(logs), 'tag' : tag}} )
        except:
            print('update error')
    except Exception as e:
        print(f'caught {e}')
        collection.update_one({ '_id': id }, { "$set" : {'status' : 'BUILD_FAILED'}} )
        print(f'Build failed for {tag}, {id}')

def _pretty(container):
    return {
        "name" : container.name,
        "id" : container.short_id, 
        "image_tags" : container.image.tags,
        "status" : container.status
        }

def get_containers(client):
    containers = client.containers.list()
    return tuple(map(lambda x: _pretty(x),containers))

def build_image(client, collection, tag, id, path, endpoint, code):
    executor.submit(async_build, client, collection, tag, id, path, endpoint, code)

def run_container(client, collection, id):
    img = collection.containers.find_one({"_id":ObjectId(id)})
    img['_id'] = str(img['_id'])
    tag = img['tag']
    print("tag = " + str(tag)) #PKDBG/Exposure
    container = client.containers.run(tag, detach = True, name = tag, network = "hambda_vlchp")
    expose_endpoint(container.id[:12], img['endpoint'])
    return str(container.logs())
    

if __name__ == "__main__":
    client = docker.from_env()
    pprint.PrettyPrinter().pprint(get_containers(client))