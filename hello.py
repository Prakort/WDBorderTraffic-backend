from flask import Flask
import requests
app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello World!'

@app.route('/hello')
def index(request):
    r = requests.get('http://httpbin.org/status/418')
    print(r.text)
    return HttpResponse('<pre>' + r.text + '</pre>')