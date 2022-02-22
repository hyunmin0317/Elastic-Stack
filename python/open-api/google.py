from pytrends.request import TrendReq

keywords = ["nft"]
pytrends = TrendReq(hl='ko', tz=360)

pytrends.build_payload(keywords, cat=0, timeframe='today 12-m', geo='KR', gprop='')
getdatainfo = pytrends.interest_over_time()
del getdatainfo['isPartial']

print(getdatainfo)