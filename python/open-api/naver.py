import json
import urllib.request
from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta
from elasticsearch import Elasticsearch, helpers

def naver_API(date):
    delta = relativedelta(years=5)
    last = date - delta
    today = date.strftime("%Y-%m-%d")
    last_year = last.strftime("%Y-%m-%d")

    client_id = "FcQj8Lu4lqN6P6O8cKUw"
    client_secret = "6b0HRiTIHX"
    url = "https://openapi.naver.com/v1/datalab/search"
    body = '''{
        "startDate": "'''+last_year+'''",
        "endDate": "'''+today+'''",
        "timeUnit": "date",
        "keywordGroups": [
            {
                "groupName": "NFT",
                "keywords": [
                    "nft"
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

def naver_NFT():
    es = Elasticsearch(['http://3.34.219.4:9200/'])
    docs = []
    list = naver_API(datetime.today())

    for data in list:
        date = data['period']
        doc = {
            "_index": "nft_search",
            "_id": "naver_"+date,
             "_source": {
                 "date": date,
                 "naver_ratio": data['ratio']
             }
        }
        docs.append(doc)
    print(docs)
    res = helpers.bulk(es, docs)
    return list[-1]['period']

print(naver_NFT())