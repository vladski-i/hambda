import docker
import pprint

TEMPLATES_PATH = './templates'

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

def build(client):
    return None

if __name__ == "__main__":
    client = docker.from_env()
    pprint.PrettyPrinter().pprint(get_containers(client))