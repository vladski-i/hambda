from flask import Flask

app = Flask(__name__)

@app.route(u"{{ endpoint }}".encode('utf-8').decode('iso-8859-1'))
def index():
{{ code }}