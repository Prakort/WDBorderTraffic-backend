from flask import Flask
from flask import request
from flask import jsonify
from bs4 import BeautifulSoup as soup
import re
from urllib.request import Request, urlopen
import requests
import json as JSON
app = Flask(__name__)
def compare(bridge, tunnel):
    try:
        tn = re.split('/', tunnel)
        bd = re.split('/',bridge)
        tn = tn[0].lower()
        bd = bd[0].lower()

        if(tn == 'no delay' and bd == 'no delay'):
            return ('No delay in either bridge or tunnel')
        elif(tn == 'no delay' and bd != 'no delay'):
            return 'There is no delay in DW Tunnel'
        elif(tn != 'no delay' and bd == 'no delay'):
            return 'There is no wait time in Ambassador Bridge'
        else:
            tn = re.sub("[^0-9]", '', tn)
            bd = re.sub("[^0-9]", '', bd)
            a = int(tn)
            b = int(bd)
            if(a > b):
                return 'Ambassador Bridge has less wait time than DW Tunnel'
            elif(a < b):
                return 'DW Tunnel has less wait time than Ambassador Bridge'
            else:
                return 'Both bridge and tunnel have same wait times'
    except:
        return 'We do not have enough information to compare'
def finalData():
    def com(time,lane):
        if lane == 0:
            return 'Closed'
        elif lane == 1:
            return str(time)+' min/'+str(lane)+ ' lane'
        else:
            return str(time)+' min/'+str(lane)+' lanes'

    api ="https://api.dwtunnel.com/api/traffic/conditionspublic"
    res = requests.get(api)
    soup1 = soup(res.content, 'html.parser')
    y = JSON.loads(soup1.text)
    j ={"USCA":y[0],"CAUS":y[1]}
        
    tUSCA = j['USCA']['DetailsTravelTime']
    tUSCA = re.sub("[^0-9]",'',tUSCA)

    T_CAR_US_CA = com(tUSCA,j['USCA']['CarLaneCount'])
    T_Nexus_US_CA = com(tUSCA,j['USCA']['NexusLaneCount'])
    T_Com_US_CA = com(tUSCA,j['USCA']['TruckLaneCount'])
    #print("USCA-->"+T_CAR_US_CA + '--'+T_Nexus_US_CA+'--'+T_Com_US_CA)

    tCAUS = j['CAUS']['DetailsTravelTime']
    tCAUS = re.sub("[^0-9]",'',tCAUS)
    T_CAR_CA_US = com(tUSCA,j['CAUS']['CarLaneCount'])
    T_Nexus_CA_US = com(tUSCA,j['CAUS']['NexusLaneCount'])
    T_Com_CA_US = com(tUSCA,j['CAUS']['TruckLaneCount'])

    data={
    "T_CAR_US_CA":T_CAR_US_CA,
    "T_Nexus_US_CA":T_Nexus_US_CA,
    "T_Com_US_CA":T_Com_US_CA,
    "T_CAR_CA_US":T_CAR_CA_US,
    "T_Nexus_CA_US":T_Nexus_CA_US,
    "T_Com_CA_US":T_Com_CA_US,
    "tCAUS":tCAUS,
    "tUSCA":tUSCA
    }
    url = 'https://www.ezbordercrossing.com/list-of-border-crossings/michigan/ambassador-bridge/current-traffic/'
    req = Request(url , headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    page_soup = soup(webpage, "html.parser")

    # getting text, finding the keyword 'delay', returning splice of string from index [delay-7:delay] where 7 is 'xx min ' length of string
    def bridge_time(a):
        if(a == ''):
            return 'No Data Available'
        else:
            delay = a.find('delay')
            no_delay = a.find('No delay')
            No_delay = a.find('no delay')
            return a[delay-7:delay] if (no_delay == -1 and No_delay == -1) else 'No delay'
    def bridge_personal_lane(a):
        close_lane = a.find('closed')
        Closed_lane = a.find('Closed')
        if(close_lane == -1 and Closed_lane == -1):
            lane = a.find('lane')    
            return '' if lane == -1 else a[lane-2:lane]+('lane open' if a[lane-2:lane] == '1 ' else 'lanes open')
        else:
            return 'Lanes closed'
    ###def bridge_personal_lane(a):
    ###   lane = a.find('lane')
    ###  return '' if lane == -1 else a[lane-2:lane]+('lane' if a[lane-2:lane] == '1 ' else 'lanes')

    # Entering Canada time
    Enter_CA_TIME = (page_soup.select('time')[0].text)[11:16]
    # Entering USA time
    Enter_US_TIME = (page_soup.select('td')[1].text)[5:9]

    # Entering Canada personal vehicles 
    Enter_US_personal_time = bridge_time(page_soup.select('td')[1].text)
    # Entering Canada personal vehicles 
    Enter_CA_personal_time = bridge_time(page_soup.select('td')[2].text)

    # Entering Canada commercial vehicles 
    Enter_US_commercial_time = bridge_time(page_soup.select('td')[10].text)
    # Entering Canada commercial vehicles 
    Enter_CA_commercial_time = bridge_time(page_soup.select('td')[11].text)

    # Entering Canada personal vehicles 
    Enter_US_personal_lane = bridge_personal_lane(page_soup.select('td')[1].text)
    # Entering US personal vehicles 
    Enter_CA_personal_lane = bridge_personal_lane(page_soup.select('td')[2].text)

    # Entering Canada commerical vehicles 
    Enter_US_commerical_lane = bridge_personal_lane(page_soup.select('td')[10].text)
    # Entering US commercial vehicles 
    Enter_CA_commercial_lane = bridge_personal_lane(page_soup.select('td')[11].text)

    # Entering Canada NEXUS 
    Enter_CA_NEXUS = bridge_time(page_soup.select('td')[5].text)
    # Entering USA NEXUS 
    Enter_US_NEXUS = bridge_time(page_soup.select('td')[4].text)
    Enter_US_NEXUS_lane = bridge_personal_lane(page_soup.select('td')[4].text)

    B_CAR_CA_US = Enter_US_personal_time+'/'+Enter_US_personal_lane
    B_CAR_US_CA = Enter_US_personal_time
    B_Com_CA_US = Enter_US_commercial_time+'/'+Enter_US_commerical_lane
    B_Com_US_CA = Enter_CA_commercial_time
    B_Nexus_CA_US = Enter_US_NEXUS+'/'+Enter_US_NEXUS_lane
    B_Nexus_US_CA = Enter_CA_NEXUS

    data["B_CAR_CA_US"]=B_CAR_CA_US
    data["B_CAR_US_CA"]=B_CAR_US_CA
    data["B_Com_CA_US"]=B_Com_CA_US
    data["B_Com_US_CA"]=B_Com_US_CA
    data["B_Nexus_CA_US"]=B_Nexus_CA_US
    data["B_Nexus_US_CA"]=B_Nexus_US_CA
    data['COMP_CAR_US_CA']=compare(data["B_CAR_US_CA"],data["T_CAR_US_CA"])
    data['COMP_CAR_CA_US']=compare(data["B_CAR_CA_US"],data["T_CAR_CA_US"])
    data['COMP_Com_US_CA']=compare(data["B_Com_US_CA"],data["T_Com_US_CA"])
    data['COMP_Com_CA_US']=compare(data["B_Com_CA_US"],data["T_Com_CA_US"])
    data['COMP_Nexus_US_CA']=compare(data["B_Nexus_US_CA"],data["T_Nexus_US_CA"])
    data['COMP_Nexus_CA_US']=compare(data["B_Nexus_CA_US"],data["T_Nexus_CA_US"])
    data['B_Time_CA_US']=Enter_US_TIME
    data['B_Time_US_CA']=Enter_CA_TIME
    data['T_Time']=re.sub('[0-9]+/[0-9]+/[0-9]+\s','',j['CAUS']["DetailsDate"])

    return data

def tunnelData():
    api ="https://api.dwtunnel.com/api/traffic/conditionspublic"
    res = requests.get(api)
    soup = BeautifulSoup(res.content, 'html.parser')
    y = JSON.loads(soup.text)
    return jsonify({'USCA': y[0],'CAUS': y[1]})
def data():
    other = "https://apps.cbp.gov/bwt/mobile.asp?action=n&pn=3800&fbclid=IwAR0wQLJXEDPuLpnvYudjQ2OkrR_9OcxYBm_U1YvJCqm5SXjNH12dYGEm8Cc"
    res = requests.get(other)
    soup1 = soup(res.text,'html.parser')
    table = soup1.find('article')
    arr = []
    for string in table.strings:
        arr.append(repr(string))
    #print(arr)
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

@app.route('/combine')
def json():
    return finalData()