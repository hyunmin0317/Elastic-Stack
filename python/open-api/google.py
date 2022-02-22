from pytrends.request import TrendReq
from elasticsearch import Elasticsearch, helpers

def google_API():
    keywords = ["nft"]
    pytrends = TrendReq(hl='ko', tz=360)

    pytrends.build_payload(keywords, cat=0, timeframe='today 5-y', geo='KR', gprop='')
    getdatainfo = pytrends.interest_over_time()

    list = []
    date_list = getdatainfo.index.to_list()
    value_list = getdatainfo['nft'].to_list()

    for i in range(len(date_list)-1):
        dic = {"date":date_list[i].strftime("%Y-%m-%d"), "ratio":value_list[i]}
        list.append(dic)
    return list

def google_NFT():
    es = Elasticsearch(['http://3.34.219.4:9200/'])
    docs = []
    list = google_API()

    for data in list:
        date = data['date']
        doc = {
            "_index": "nft_search",
            "_id": "google_"+date,
            "_source": {
                "date": date,
                "google_ratio": data['ratio']
            }
        }
        docs.append(doc)
    res = helpers.bulk(es, docs)
    return list[-1]['date']

print(google_NFT())