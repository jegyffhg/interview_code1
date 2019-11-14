import requests
from lxml import etree
import re
import pymongo
import time

client = pymongo.MongoClient('localhost', 27017)
dbAddress = client['dbAddress']
addressInfo = dbAddress['addressInfo']

headers = {
    #'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
}

def get_url_address(url):
    html = requests.get(url, headers=headers)
    selector = etree.HTML(html.text)
    music_hrefs = selector.xpath('//li[@class="pull-left infoContent"]/h3/a/@href')
    for address_href in music_hrefs:
        get_address_info(address_href)

def get_address_info(url):
    html = requests.get('http:'+url, headers=headers)
    selector = etree.HTML(html.text)
    renter = selector.xpath('//*[@class="avatarRight"]/div/i/text()')[0]
    homeowner = selector.xpath('//*[@class="avatarRight"]/div/text()')[0]
    phone = selector.xpath('//span[@class="num"]/text()')[0]
    type = selector.xpath('//ul[@class="attr"]/li[3]/text()')
    situation = selector.xpath('//ul[@class="attr"]/li[4]/text()')
    sex = selector.xpath('//ul[@class="clearfix labelList labelList-1"]/li[7]/div[@class="two"]/em/text()')
    print(renter, homeowner, phone, type, situation, sex)
    info = {
        'renter': renter,
        'homeowner': homeowner,
        'phone': phone,
        'type': type,
        'situation': situation,
        'sex': sex
    }

    addressInfo.insert_one(info)
        
if __name__ == '__main__':
    urls = ['https://rent.591.com.tw/?kind=0&region=1']
    for url in urls:
        get_url_address(url)
        time.sleep(2)