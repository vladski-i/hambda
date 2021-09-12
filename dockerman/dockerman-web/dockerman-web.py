from flask import Flask, request
from container_delegate import get_containers, build_image, run_container
from pymongo import MongoClient
from bson.objectid import ObjectId
from template_delegate import new_image
import docker
import pprint
import json
from nginx_delegate import init_nginx_parser

app = Flask(__name__)
docker_client = docker.from_env()
mongo_client = MongoClient(host='9de267ffefdf')
db = mongo_client.containers
init_nginx_parser()

@app.route("/dockerman/containers", methods = ['GET'])
def containers():
    return {"containers" : get_containers(docker_client)}

@app.route("/dockerman/build", methods = ['POST'])
def build():
    json = request.get_json()
    result = db.containers.insert_one({ 'name' : json['name'], 'tag' : json['tag'] ,'status' : 'BUILDING', 'endpoint': json['endpoint'] })
    path = new_image(str(result.inserted_id))
    build_image(docker_client, db.containers, json['tag'], result.inserted_id, path, json['endpoint'], json['code'])
    return {'id' : str(result.inserted_id), 'status' : 'BUILDING'}

@app.route("/dockerman/run", methods = ['POST'])
def run():
    json = request.get_json()
    id = json['id']
    return {'logs' : run_container(docker_client, db, id)}


@app.route("/dockerman/images/status", methods = ['GET'])
def status():
    json = request.get_json()
    result = db.containers.find_one({"_id":ObjectId(json['id'])})
    pprint.pprint(result)
    id = str(result['_id'])
    status = result['status']
    response = {'id' : id, 'status' : status}
    if status == 'FINISHED':
        response['logs'] = result['logs']
    return response