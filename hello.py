from flask import Flask
from flask import request
from flask import jsonify
from bs4 import BeautifulSoup
import requests
app = Flask(__name__)

quarks = [{'name': 'up', 'charge': '+2/3'},
          {'name': 'down', 'charge': '-1/3'},
          {'name': 'charm', 'charge': '+2/3'},
          {'name': 'strange', 'charge': '-1/3'}]

@app.route('/',methods=['GET'])
def hello():
    return 'Hello World!'

@app.route('/hello')
def index(request):
    r = requests.get('http://httpbin.org/status/418')
    print(r.text)
    return HttpResponse('<pre>' + r.text + '</pre>')

@app.route('/data')
def data(request):
    other = "https://apps.cbp.gov/bwt/mobile.asp?action=n&pn=3800&fbclid=IwAR0wQLJXEDPuLpnvYudjQ2OkrR_9OcxYBm_U1YvJCqm5SXjNH12dYGEm8Cc"
    res = requests.get(other)
    soup = BeautifulSoup(res.text,'html.parser')
    table = soup.find('article')
    arr = []
    for string in table.strings:
        arr.append(repr(string))
    return arr
@app.rout('/json',methods=['GET'])
def json():
    return jsonify({'quarks': quarks})