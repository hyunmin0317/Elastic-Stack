from pytrends.request import TrendReq
from elasticsearch import Elasticsearch, helpers

def google_NFT(word):
    es = Elasticsearch(['http://3.34.219.4:9200/'])
    docs = []
    dict = {}

    keywords = [word]
    pytrends = TrendReq(hl='ko', tz=300)
    pytrends.build_payload(keywords, cat=0, timeframe='today 1-m', geo='', gprop='')
    by_region = pytrends.interest_by_region(resolution='COUNTRY', inc_geo_code=True)

    key_list = by_region['geoCode'].to_list()
    geo_list = by_region.index.to_list()
    value_list = by_region['nft'].to_list()

    for i in range(len(key_list)):
        dict[key_list[i]] = [geo_list[i], value_list[i]]

    for key in dict.keys():
        doc = {
            "_index": "world_nft",
            "_id": key,
            "_source": {
                "country": dict[key][0],
                "ratio": dict[key][1]
            }
        }
        docs.append(doc)
    res = helpers.bulk(es, docs)
    print(docs)

google_NFT('nft')