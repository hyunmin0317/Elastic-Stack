import json
import urllib.request
from datetime import datetime, timedelta

def naver_API(date):
    today = date.strftime("%Y-%m-%d")
    print(today)

    client_id = "FcQj8Lu4lqN6P6O8cKUw"
    client_secret = "6b0HRiTIHX"
    url = "https://openapi.naver.com/v1/datalab/search"
    body = '''{
        "startDate": "2021-02-22",
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
    print(body)

    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    request.add_header("Content-Type","application/json")
    response = urllib.request.urlopen(request, data=body.encode("utf-8"))

    response_body = response.read().decode('utf-8')
    data = json.loads(response_body)['results'][0]['data']
    return data

print(naver_API(datetime.today()))

today = datetime.today() - timedelta(365)
date = today.strftime("%Y-%m-%d")
print(date)