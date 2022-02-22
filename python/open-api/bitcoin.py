import json
import urllib.request
from datetime import datetime
import FinanceDataReader as fdr
from elasticsearch import Elasticsearch, helpers

def naver_API(start, end):
    today = end.strftime("%Y-%m-%d")

    client_id = "FcQj8Lu4lqN6P6O8cKUw"
    client_secret = "6b0HRiTIHX"
    url = "https://openapi.naver.com/v1/datalab/search"
    body = '''{
        "startDate": "'''+start+'''-01-01",
        "endDate": "'''+today+'''",
        "timeUnit": "date",
        "keywordGroups": [
            {
                "groupName": "비트코인",
                "keywords": [
                    "비트코인",
                    "bitcoin"
                ]
            }
        ]
    }'''

    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    request.add_header("Content-Type","application/json")
    response = urllib.request.urlopen(request, data=body.encode("utf-8"))

    response_body = response.read().decode('utf-8')
    data = json.loads(response_body)['results'][0]['data']
    return data

def coin(name, date):
    df = fdr.DataReader(name, date)
    date_list = df.index.to_list()
    value_list = df['Close'].to_list()
    list = []


    for i in range(len(date_list)-1):
        dic = {"date":date_list[i].strftime("%Y-%m-%d"), "price":value_list[i]}
        list.append(dic)
    return list

def coin_data(name, start):
    es = Elasticsearch(['http://3.34.219.4:9200/'])
    docs = []
    search_list = naver_API(start, datetime.today())
    price_list = coin(name, start)

    for i in range(len(search_list)):
        date = price_list[i]['date']
        doc = {
            "_index": "coin",
            "_id": name+date,
            "_source": {
                "date": date,
                "search": search_list[i]['ratio'],
                "price": price_list[i]['price']
            }
        }
        docs.append(doc)
    res = helpers.bulk(es, docs)

coin_data('BTC/KRW', '2020')