import requests
import re
import json


session_requests = requests.session()
res = session_requests.get('https://rent.591.com.tw/?kind=0&region=1')

csrfTokenMeta = re.findall('<meta name="csrf-token" content="[a-zA-Z0-9]*">' ,str(res.content))[0]
csrfToken = csrfTokenMeta[csrfTokenMeta.index("content=") + 9: len(csrfTokenMeta) - 2]

def getHeaders():
    return {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0",
        "Accept":"application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "zh-TW,zh;q=0.8,en-US;q=0.5,en;q=0.3",
        "Accept-Encoding": "gzip, deflate, br",
        "X-CSRF-TOKEN": csrfToken,
        "X-Requested-With": "XMLHttpRequest",
        "Connection": "keep-alive",
        "Referer": "https://rent.591.com.tw/?kind=0&region=15",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
    }


def nextPage():
    res = session_requests.get('https://rent.591.com.tw/home/search/rsList?is_new_list=1&type=1&kind=0&searchtype=1&region=15', headers = getHeaders())
    jsonContent = json.loads(res.content)
    maxRow = int(jsonContent["records"].replace("," , "")) - 1
    row = len(jsonContent["data"]["data"])
    urls = ("https://rent.591.com.tw/rent-detail-{}.html".format(x["post_id"]) for x in jsonContent["data"]["data"])
    yield urls
    
    while(row < maxRow):
        res = session_requests.get('https://rent.591.com.tw/home/search/rsList?is_new_list=1&type=1&kind=0&searchtype=1&region=15&firstRow={}&totalRows=2825'.format(row), headers = getHeaders())
        jsonContent = json.loads(res.content)
        row += len(jsonContent["data"]["data"])
        urls = ("https://rent.591.com.tw/rent-detail-{}.html".format(x["post_id"]) for x in jsonContent["data"]["data"])
        yield urls

count = 1
for urls in nextPage():
    for url in urls:
        #print(str(count) + ":" + url)
        count += 1
