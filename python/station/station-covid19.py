import urllib.request
from xml.etree.ElementTree import fromstring, ElementTree
from elasticsearch import Elasticsearch, helpers
import csv
from datetime import datetime, timedelta

es = Elasticsearch(['http://3.34.219.4:9200/'])

def covid19():
    seoul = {"JONGNOADD":"종로구", "JUNGGUADD":"중구", "YONGSANADD":"용산구", "SEONGDONGADD":"성동구", "GWANGJINADD":"광진구", "DDMADD":"동대문구", "JUNGNANGADD":"중랑구", "SEONGBUKADD":"성북구", "GANGBUKADD":"강북구", "DOBONGADD":"도봉구", "NOWONADD":"노원구", "EPADD":"은평구", "SDMADD":"서대문구", "MAPOADD":"마포구", "YANGCHEONADD":"양천구", "GANGSEOADD":"강서구", "GUROADD":"구로구", "GEUMCHEONADD":"금천구", "YDPADD":"영등포구", "DONGJAKADD":"동작구", "GWANAKADD":"관악구", "SEOCHOADD":"서초구", "GANGNAMADD":"강남구", "SONGPAADD":"송파구", "GANGDONGADD":"강동구", "ETCADD":"기타"}
    covid = {}

    url = 'http://openapi.seoul.go.kr:8088/547171685163686f35324270474f6e/xml/TbCorona19CountStatusJCG/1/1/'
    response = urllib.request.urlopen(url)
    xml_str = response.read().decode('utf-8')

    tree = ElementTree(fromstring(xml_str))
    root = tree.getroot()

    for row in root.iter("row"):
        for r in row:
            if r.tag in seoul:
                covid[seoul[r.tag]] = int(r.text)
    return covid

def date():
    for i in range(100):
        today = datetime.today() - timedelta(i)
        date = today.strftime("%Y%m%d")
        url = 'http://openapi.seoul.go.kr:8088/547171685163686f35324270474f6e/xml/CardSubwayStatsNew/1/600/'+date

        response = urllib.request.urlopen(url)
        xml_str = response.read().decode('utf-8')
        tree = ElementTree(fromstring(xml_str))
        root = tree.getroot()

        for row in root.iter("MESSAGE"):
            if row.text == '정상 처리되었습니다':
                return date

def station_data():
    f = open('station_info.csv', 'r')
    rdr = csv.reader(f)

    info = {}
    data = []

    for line in rdr:
        data.append(line)
    f.close()

    for d in data:
        station = d[2].split()

        if station[0] == '서울특별시':
            info[d[1]] = station[1]

    return info

def subway_data():
    f = open('subway.csv', 'r', encoding='utf-8-sig')
    rdr = csv.reader(f)

    data = []

    for line in rdr:
        data.append(line)
    f.close()
    return data

def update_station():
    url = 'http://openapi.seoul.go.kr:8088/547171685163686f35324270474f6e/xml/CardSubwayStatsNew/1/600/'+date()
    es = Elasticsearch(['http://15.165.109.114:9200/'])

    data = subway_data()
    staion_info = station_data()
    covid = covid19()
    docs = []
    stations = []

    response = urllib.request.urlopen(url)
    xml_str = response.read().decode('utf-8')
    tree = ElementTree(fromstring(xml_str))
    root = tree.getroot()

    for row in data:
        station = row[1]
        place_x = row[3]
        place_y = row[4]

        if place_x != '' and place_y != '':
            place_x = float(place_x)
            place_y = float(place_y)
            info = {"station": station, "place_x": place_x, "place_y": place_y}
            stations.append(info)

    for row in root.iter("row"):
        station = row.find('SUB_STA_NM').text

        for info in stations:
            if station == info['station']:
                if station in staion_info:
                    line = row.find('LINE_NUM').text
                    ride = int(row.find('RIDE_PASGR_NUM').text)
                    alight = int(row.find('ALIGHT_PASGR_NUM').text)
                    move = ride + alight
                    place_x = info['place_x']
                    place_y = info['place_y']
                    region = staion_info[station]

                    doc = {
                        "_index": "station-covid19",
                        "_id": station,
                        "_source": {
                            "line": line,
                            "region": region,
                            "confirmed": covid[region],
                            "station": station,
                            "location": {
                                "lat": place_x,
                                "lon": place_y
                            },
                            "ride": ride,
                            "alight": alight,
                            "move": move
                        }
                    }
                    docs.append(doc)

    res = helpers.bulk(es, docs)
    print("END")