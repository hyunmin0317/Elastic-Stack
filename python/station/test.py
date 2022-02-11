import urllib.request
from datetime import datetime, timedelta
from xml.etree.ElementTree import ElementTree, fromstring

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

print(date())