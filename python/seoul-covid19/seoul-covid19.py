import urllib.request
from xml.etree.ElementTree import fromstring, ElementTree
from elasticsearch import Elasticsearch, helpers

es = Elasticsearch(['http://3.34.219.4:9200/'])

seoul = {"JONGNO":"종로구", "JUNGGU":"중구", "YONGSAN":"용산구", "SEONGDONG":"성동구", "GWANGJIN":"광진구", "DDM":"동대문구", "JUNGNANG":"중랑구", "SEONGBUK":"성북구", "GANGBUK":"강북구", "DOBONG":"도봉구", "NOWON":"노원구", "EP":"은평구", "SDM":"서대문구", "MAPO":"마포구", "YANGCHEON":"양천구", "GANGSEO":"강서구", "GURO":"구로구", "GEUMCHEON":"금천구", "YDP":"영등포구", "DONGJAK":"동작구", "GWANAK":"관악구", "SEOCHO":"서초구", "GANGNAM":"강남구", "SONGPA":"송파구", "GANGDONG":"강동구", "ETC":"기타"}
seoul_add = {"JONGNOADD":"종로구", "JUNGGUADD":"중구", "YONGSANADD":"용산구", "SEONGDONGADD":"성동구", "GWANGJINADD":"광진구", "DDMADD":"동대문구", "JUNGNANGADD":"중랑구", "SEONGBUKADD":"성북구", "GANGBUKADD":"강북구", "DOBONGADD":"도봉구", "NOWONADD":"노원구", "EPADD":"은평구", "SDMADD":"서대문구", "MAPOADD":"마포구", "YANGCHEONADD":"양천구", "GANGSEOADD":"강서구", "GUROADD":"구로구", "GEUMCHEONADD":"금천구", "YDPADD":"영등포구", "DONGJAKADD":"동작구", "GWANAKADD":"관악구", "SEOCHOADD":"서초구", "GANGNAMADD":"강남구", "SONGPAADD":"송파구", "GANGDONGADD":"강동구", "ETCADD":"기타"}

covid = []
covid_add = []

url = 'http://openapi.seoul.go.kr:8088/547171685163686f35324270474f6e/xml/TbCorona19CountStatusJCG/1/1/'
response = urllib.request.urlopen(url)
xml_str = response.read().decode('utf-8')

tree = ElementTree(fromstring(xml_str))
root = tree.getroot()

for row in root.iter("row"):
    for r in row:
        if r.tag in seoul:
            region = seoul[r.tag]

            doc = {
                "_index": "seoul-covid19",
                "_id": region,
                "_source": {
                    "region": region,
                    "confirmed": int(r.text),
                }
            }
            covid.append(doc)
        elif r.tag in seoul_add:
            region = seoul_add[r.tag]
            doc = {
                "_index": "seoul-covid19-add",
                "_id": r.tag,
                "_source": {
                    "region": region,
                    "confirmed": int(r.text),
                }
            }
            covid_add.append(doc)

res = helpers.bulk(es, covid)
res = helpers.bulk(es, covid_add)
print("END")