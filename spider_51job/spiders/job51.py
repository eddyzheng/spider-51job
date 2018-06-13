#coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import scrapy
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
from spider_51job.items import Spider51JobItem

class DmozSpider(scrapy.spiders.Spider):
    name = "51job"
    # allowed_domains = ["51job.com"]
    start_urls = [
        "https://search.51job.com/list/020000,000000,0000,32,9,99,%25E5%2589%258D%25E7%25AB%25AF%25E5%25BC%2580%25E5%258F%2591,2,1.html?lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare=",
    ]

    def parse(self, response):
       el = response.xpath('//*[@id="resultList"]/div[@class="el"]').extract()
       lineNum = len(el)
       for val in el:
           obj = Selector(text=val)
           title = obj.xpath('//p/span/a/text()').extract()[0]
           com = obj.xpath('//span[@class="t2"]/a/text()').extract()[0]
           location = obj.xpath('//span[@class="t3"]/text()').extract()[0]
           salaryList = obj.xpath('//span[@class="t4"]/text()').extract()
           time = obj.xpath('//span[@class="t5"]/text()').extract()[0]
           salary = 1
           if len(salaryList) == 1:
               salary = salaryList[0]

           dic =  {
                "title": title,
                "com" : com,
                "location" :location,
                "time" : time,
                "salary" : salary
               }
           yield Spider51JobItem(dic)
       Lurl = response.url.split('?')
       start = Lurl[0].rfind(',')
       end = Lurl[0].rfind('.')
       pNum = Lurl[0][start+1:end]
       nextpageNum = str(int(pNum) + 1)
       nextUrl = Lurl[0][:start+1] + nextpageNum + '.html?' + Lurl[1]
       print 'nextUrl:'
       print nextUrl
       yield scrapy.Request(nextUrl, callback=self.parse)