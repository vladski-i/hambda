from flask import Flask, request
from docker_interface import get_containers
import docker
import json

app = Flask(__name__)
docker_client = docker.from_env()

@app.route("/dockerman/containers", methods = ['GET'])
def containers():
    return {"containers" : get_containers(docker_client)}

@app.route("/dockerman/build", methods = ['POST'])
def build():
    print(request.get_json())
    return {}