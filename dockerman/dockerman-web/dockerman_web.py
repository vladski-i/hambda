from flask import Flask, request
from container_delegate import get_containers, build_image, run_container, clean
from pymongo import MongoClient
from bson.objectid import ObjectId
from template_delegate import new_image
import docker
import pprint
import json
from nginx_delegate import init_nginx_parser
from config import get_containers_collection, get_docker_client
from flask_cors import cross_origin, CORS

app = Flask(__name__)
CORS(app)
docker_client = get_docker_client()
db = get_containers_collection()

init_nginx_parser()

clean()

python_flask = {
    'name' : 'python-flask',
    'code' : 'def index():\n',
    'language' : 'python'
}
java_micronaut = {
    'name' : 'java-micronaut',
    'code' : 'public String hello()\n {\n\treturn "hello";\n}',
    'language' : 'java'
}
templates_list = [python_flask, java_micronaut]

def get_docker_client():
    return docker_client

def get_container_db():
    return db

@cross_origin
@app.route("/dockerman/containers", methods = ['GET'])
def containers():
    return {"containers" : get_containers()}

@cross_origin
@app.route("/dockerman/build", methods = ['POST'])
def build():
    json = request.get_json()
    endpoint = json['endpoint']
    name = endpoint.replace('/','')
    tag = endpoint.replace('/','-')[1:]
    result = db.containers.insert_one({ 'name' : name, 'tag' : tag ,'status' : 'BUILDING', 'endpoint': endpoint })
    path = new_image(str(result.inserted_id))
    print(f'Code received is: {json["code"]}//end code')
    build_image( tag, result.inserted_id, path, json['endpoint'], json['code'])
    return {'id' : str(result.inserted_id), 'status' : 'BUILDING'}

@cross_origin
@app.route("/dockerman/run", methods = ['POST'])
def run():
    json = request.get_json()
    id = json['id']
    return {'logs' : run_container(id)}

@cross_origin
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

@cross_origin
@app.route("/dockerman/images/templates", methods = ['GET'])
def templates():
    return {'templates': templates_list}