try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen
import json
import time

def get_data():
    url = "https://tygia.com/json.php?ran=0&rate=0&gold=1&bank=VIETCOM&date=now"
    response = urlopen(url)
    data = json.loads(response.read())
    with open('data.json', 'w') as f:
        json.dump(data, f)

def update_data():
    t = time.localtime(time.time())
    min = t.tm_min
    sec = t.tm_sec
    if((min == 30 and sec == 0) or (min == 0 and sec == 0)):
        get_data()

def read_data():
    with open("data.json", "r") as fin:
        data = json.load(fin)
    return data

def search(str):
    data = read_data()
    for i in data['golds'][0]['value']:
        if (str == data['golds'][0]['value'][i]['brand']):
            company = data['golds'][0]['value'][i]['company']
            brand = data['golds'][0]['value'][i]['brand']
            sell = data['golds'][0]['value'][i]['sell']
            buy = data['golds'][0]['value'][i]['buy']
            return company, brand, sell, buy

get_data()