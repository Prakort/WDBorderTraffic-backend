from flask import Flask
from flask import request
from flask import jsonify
from bs4 import BeautifulSoup
import requests
import json as JSON
app = Flask(__name__)
def tunnelData():
    api ="https://api.dwtunnel.com/api/traffic/conditionspublic"
    res = requests.get(api)
    soup = BeautifulSoup(res.content, 'html.parser')
    y = JSON.loads(soup.text)
    print(y)
    return y
def data():
    other = "https://apps.cbp.gov/bwt/mobile.asp?action=n&pn=3800&fbclid=IwAR0wQLJXEDPuLpnvYudjQ2OkrR_9OcxYBm_U1YvJCqm5SXjNH12dYGEm8Cc"
    res = requests.get(other)
    soup = BeautifulSoup(res.text,'html.parser')
    table = soup.find('article')
    arr = []
    for string in table.strings:
        arr.append(repr(string))
    print(arr)
    return jsonify({'arr': arr})

quarks = [{'name': 'up', 'charge': '+2/3'},
          {'name': 'down', 'charge': '-1/3'},
          {'name': 'charm', 'charge': '+2/3'},
          {'name': 'strange', 'charge': '-1/3'}]

@app.route('/',methods=['GET'])
def hello():
    return 'Hello World!'

@app.route('/tunnel')
def sendtunnel():
    return tunnelData()

@app.route('/data')
def dataone():
    return data()

@app.route('/json',methods=['GET'])
def json():
    return jsonify({'quarks': quarks})