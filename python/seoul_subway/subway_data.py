import urllib.request
from xml.etree.ElementTree import fromstring, ElementTree
from elasticsearch import Elasticsearch, helpers

es = Elasticsearch(['http://15.165.109.114:9200/'])

stations = []
docs = []
url = 'http://openapi.seoul.go.kr:8088/547171685163686f35324270474f6e/xml/CardSubwayStatsNew/1/600/20220203'
response = urllib.request.urlopen(url)
xml_str = response.read().decode('utf-8')

tree = ElementTree(fromstring(xml_str))
root = tree.getroot()


for row in root.iter("row"):
    line = row.find('LINE_NUM').text
    station = row.find('SUB_STA_NM').text
    ride = int(row.find('RIDE_PASGR_NUM').text)
    alight = int(row.find('ALIGHT_PASGR_NUM').text)

    doc = {
        "_index": "subway",
        "_id": station,
        "_source": {
            "line": line,
            "station": station,
            "ride": ride,
            "alight": alight
        }
    }
    docs.append(doc)

res = helpers.bulk(es, docs)
print("END")