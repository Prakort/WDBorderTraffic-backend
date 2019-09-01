from flask import Flask
from bs4 import BeautifulSoup
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

@app.route('data')
def data():
    other = "https://apps.cbp.gov/bwt/mobile.asp?action=n&pn=3800&fbclid=IwAR0wQLJXEDPuLpnvYudjQ2OkrR_9OcxYBm_U1YvJCqm5SXjNH12dYGEm8Cc"
    res = requests.get(other)
    soup = BeautifulSoup(res.text,'html.parser')
    table = soup.find('article')
    arr = []
    for string in table.strings:
        arr.append(repr(string))
    return arr
