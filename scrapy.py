import requests
import json
import re
import time
from datetime import datetime


def search_prods(query, price):
    headers = {
        'cookie': 'ECC=d911495b10631cebd0d52600fe5f47243f42a637.1595662688; _gcl_au=1.1.1898070603.1595662690; _gid=GA1.3.1152224535.1595662692; venguid=e3f97364-728b-430c-ba6e-60b57efc96e8.wg1-1n4020200725; U=3a970d59a80440caa47553ec4bf745db326b8f02; ECWEBSESS=9696a9c425.f59f90cba2642d299ebf735a4fa4ff7ba1ba6ba9.1595684293; G_PH=["DJAA2V-A90092SFL"]; vensession=b10cda67-ca7f-46c8-a95d-1207b8588ad6.wg1-1n4020200725.se; _ga=GA1.1.148710659.1595662690; _ga_9CE1X6J1FG=GS1.1.1595689986.4.1.1595694711.0',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}

    # 每次加載分頁有20筆資料，可以依需求增加/減少
    pages = 2

    # get prods list
    prodids = []
    for page in list(range(1, pages)):
        url = 'https://ecshweb.pchome.com.tw/search/v3.3/all/results?q={}&page={}&sort=sale/dc'.format(
            query, page)
        # every time request after sleep time 2s
        time.sleep(2)
        resp = requests.get(url, headers=headers)
        data = resp.json()
        if data:
            for prod in data['prods']:
                regex = query.split('-')
                validToken = re.search(query, prod['name'])
                validToken1 = re.search(regex[0], prod['name'])
                validToken2 = re.search(regex[0] + '-', prod['name'])
                if validToken:
                    if(int(price) > prod['price']):
                        return {'price': price, 'lowestPrice': prod['price'], 'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
                elif validToken1 and (not validToken2):
                    if(int(price) > prod['price']):
                        return {'price': price, 'lowestPrice': prod['price'], 'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")}