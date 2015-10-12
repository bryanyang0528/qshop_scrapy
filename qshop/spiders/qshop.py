import sys
import re
import scrapy
from datetime import datetime
from scrapy.http import Request, FormRequest, TextResponse
from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy import log
from ..items import QshopItem


class Crawler(CrawlSpider):
    name = "qshop"
    allowed_domains = ["myqshop.com.tw"]
    start_urls = [
        "http://www.myqshop.com.tw/"
    ]

    rules = [
        Rule(LinkExtractor(allow = ('\pdlist2.asp?\w+.*')),
        follow = True),

        Rule(LinkExtractor(allow = ('\PDContent.asp?\w+.*')),
        callback = 'parse_table', follow = False)
     ]

    def parse_table(self, response):
        item = QshopItem()
        sel = Selector(response)

        # give default value
        for i in item:
            item[i] = ''

       
        #print sel.extract()
        item['date'] = datetime.now().strftime("%Y-%m-%d")
        
        #get item from link
        link = response.url
	item_list=link.split('?')[1].split("&")
        print item_list
        for i in item_list:
            i = i.split("=")
            item[i[0]] = i[1].encode('utf-8').strip()

        #category name

        if item['item1'] != '' and item['item2'] != '':
            item1_link = "PDList2.asp?item1=" + item['item1'] 
            item2_link = "PDList2.asp?item1=" + item['item1'] + "&item2=" + item['item2']
            #item['item1_ch'] = sel.xpath('//a[@href="%s"]/text()'% (item1_link))[0].extract().encode('utf-8').strip()
            #item['item2_ch'] = sel.xpath('//a[@href="%s"]/text()'% (item2_link))[0].extract().encode('utf-8').strip()

            try:
                item['item1_ch'] = sel.xpath('//a[starts-with(@href, "PDList2.asp?item1=")]/text()')[0].extract().encode('utf-8').strip()
            except IndexError as e:
                item['item1_ch'] =''

            try:
                item['item2_ch'] = sel.xpath('//a[starts-with(@href, "PDList2.asp?item1=")]/text()')[1].extract().encode('utf-8').strip()
	    except IndexError as e:
                item['imte2_ch'] = ''
        else:
	    item['item1_ch'] = ''
            item['item2_ch'] = ''


        #get item from html
        table = sel.xpath('//div[@id="pdinfo"]')
 
        item['pdName'] = table.xpath('.//div[@id="pdNameA"]/text()')[0].extract().encode('utf-8').strip()
        item['pdno'] = table.xpath('.//div[@id="pdno"]/span/text()')[1].extract().strip()
        item['pdsales'] = table.xpath('.//div[@id="pdsales"]/span/text()')[1].extract().strip()
        
        try:
            item['price'] = re.sub(r'^\$.', "",table.xpath('.//div[@class="price"]/span/text()')[1].extract()).strip()
        except IndexError as e:
            item['price'] = ''

        try:
            item['priceOriginal'] = re.sub(r'^\$.', "",table.xpath('.//span[@class="priceOriginal"]/text()')[1].extract()).strip()
            item['priceNormal'] = re.sub(r'^\$.', "",table.xpath('.//span[@class="priceNormal"]/text()')[1].extract()).strip()
        except IndexError as e:
            item['priceOriginal'] = ''
            item['priceNormal'] = ''

        yield item

