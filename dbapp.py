import requests
import schedule
import time
import psycopg2
import json
from config2 import config

def get_prices(url):
    urlFull = 'https://api.coingecko.com/api/v3/simple/price?ids=' + url + '&vs_currencies=usd&include_24hr_change=true'
    # print(urlFull)
    # r =requests.get('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin%2Cethereum&vs_currencies=usd')
    r = requests.get(urlFull)
    return(r.json())

def get_holdings():
    r1 =requests.get('http://127.0.0.1:5000/holdings')
    # r1 =requests.get('http://192.168.1.70:5000/holdings')
    # Form URL from holdings
    
    total=0
    # print(r1.text)
    myHoldingsDict = r1.json()
    myHoldingsList = myHoldingsDict['holdings']
    # myPricesDict = get_prices()
    # print(myPricesDict)
    urlText = ''
    for holding in myHoldingsList:
        urlText = urlText +  holding['name'] + '%2C'

    pricesDict = get_prices(urlText)

    for k,v in pricesDict.items():
        for myHolding in myHoldingsList:
            if (k == myHolding['name']): 
                # print(' ')
                # print(myHolding['amount'])
                # print(k);
                # print(v['usd'])
                # print("24 hour change")
                # print(v['usd_24h_change'])
                # bodyDict = {'name': 'ethereum', 'id': 'ETH', 'amount': 0, 'last_price': 1.0}
                formatShortChange = f"{v['usd_24h_change']:.2}"
                # print(formatShortChange)
                bodyDict = {"name": k, "id": myHolding['id'], "amount": myHolding['amount'], "last_price": v['usd'], "day_change": formatShortChange}
                update_prices(k, bodyDict)
                total = total + (myHolding['amount'] * v['usd'])
                print(k, myHolding['amount'] * v['usd'])               
                print(k, myHolding['last_price'])
                # url = 'http://127.0.0.1:5000/holdings'
                # x = requests.post(url, json = json.dumps(myobj))
                # print(x.text)               
    epoch_time = int(time.time())
    totalhistBody = {'time_stamp': epoch_time, 'amount': int(total)}
    # update_totalhists(totalhistBody)
    print(totalhistBody)
                       
def update_prices(name, body):
    # body = {"name": "bitcoin", "id": "BTC", "amount": 500, "last_price": 2.5}
    # print(body)
    url = 'http://192.168.1.70:5000/prices/' + name
    r1 =requests.put(url, json=json.dumps(body))
    # print(r1)

def update_totalhists(body):
    print(body)
    toSend = json.dumps(body)
    # print(type(body))
    # url = 'http://127.0.0.1:5000/totalhist'
    url = 'http://192.168.1.70:5000/totalhist'
    #r1 =requests.post(url, json=json.dumps(body))
    r1 =requests.post(url, json=body)
    # print(r1)

# if __name__ == '__main__':
get_holdings()
# schedule.every(15).minutes.do(get_holdings)
#put_24_price()

# while True:
#     schedule.run_pending()
#     time.sleep(1)
