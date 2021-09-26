import docker
from pymongo import MongoClient
from functools import lru_cache

client = docker.from_env()
containers = MongoClient(host='eff584884f8c').containers

@lru_cache(maxsize=None)
def get_docker_client():
    return client

@lru_cache(maxsize=None)
def get_containers_collection():
    return containers