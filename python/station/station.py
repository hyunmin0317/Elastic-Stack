import csv
import urllib.request
from xml.etree.ElementTree import fromstring, ElementTree
from elasticsearch import Elasticsearch, helpers

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

if '__main__':
    url = 'http://openapi.seoul.go.kr:8088/547171685163686f35324270474f6e/xml/CardSubwayStatsNew/1/600/20220203'
    es = Elasticsearch(['http://15.165.109.114:9200/'])

    data = subway_data()
    staion_info = station_data()
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
                    place_x = info['place_x']
                    place_y = info['place_y']

                    doc = {
                        "_index": "station",
                        "_id": station,
                        "_source": {
                            "line": line,
                            "region": staion_info[station],
                            "station": station,
                            "location": {
                                "lat": place_x,
                                "lon": place_y
                            },
                            "ride": ride,
                            "alight": alight
                        }
                    }
                    docs.append(doc)

    res = helpers.bulk(es, docs)
    print("END")