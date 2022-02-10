import urllib.request
from xml.etree.ElementTree import fromstring, ElementTree
from elasticsearch import Elasticsearch, helpers

es = Elasticsearch(['http://3.34.219.4:9200/'])

docs = []

url = 'http://openapi.seoul.go.kr:8088/547171685163686f35324270474f6e/xml/TbCorona19CountStatus/1/400/'
response = urllib.request.urlopen(url)
xml_str = response.read().decode('utf-8')

tree = ElementTree(fromstring(xml_str))
root = tree.getroot()

for row in root.iter("row"):
    date = row.find('S_DT').text
    today = int(row.find('N_HJ').text)
    confirmed = int(row.find('T_HJ').text)
    death = int(row.find('DEATH').text)
    recover = int(row.find('RECOVER').text)
    doc = {
        "_index": "covid19_logstash",
        "_id": date,
        "_source": {
            "date": date,
            "today": today,
            "confirmed": confirmed,
            "death": death,
            "recover": recover
        }
    }
    docs.append(doc)

res = helpers.bulk(es, docs)
print("END")