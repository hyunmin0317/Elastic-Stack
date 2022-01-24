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
    es = Elasticsearch(['http://34.64.136.175:9200/'])

    data = subway_data()
    docs = []

    i = 0
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
                "_index": "seoul_subway",
                "_id": i,
                "_source": {
                    "line": line,
                    "station": station,
                    "number": number,
                    "instl_xy": {
                        "lat": place_x,
                        "lon": place_y
                    }
                }
            }
            i += 1
            docs.append(doc)

res = helpers.bulk(es, docs)
print("END")