import csv
import urllib.request
from xml.etree.ElementTree import fromstring, ElementTree
from elasticsearch import Elasticsearch, helpers

def subway_data():
    f = open('subway.csv', 'r', encoding='utf-8-sig')
    rdr = csv.reader(f)

    data = []

    for line in rdr:
        data.append(line)
    f.close()
    return data

if '__main__':
    es = Elasticsearch(['http://15.165.109.114:9200/'])

    data = subway_data()
    docs = []

    for row in data:
        line = row[0]
        station = row[1]
        number = row[2]
        place_x = row[3]
        place_y = row[4]

        if place_x != '' and place_y != '':
            place_x = float(place_x)
            place_y = float(place_y)

            doc = {
                "_index": "subway",
                "_id": station,
                "_source": {
                    "line": line,
                    "station": station,
                    "number": number,
                    "location": {
                        "lat": place_x,
                        "lon": place_y
                    },
                    "ride": 0,
                    "alight": 0
                }
            }
            docs.append(doc)

res = helpers.bulk(es, docs)
print("END")