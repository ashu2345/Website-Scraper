# -*- coding: utf-8 -*-
import scrapy
import re


class DataSpider(scrapy.Spider):
    name = 'data'
    allowed_domains = ['healthyceleb.com/']
    start_urls = ['https://healthyceleb.com/category/statistics/sports-stars/male-sports-stars/']
    count = 0

    def parse(self, response):
        links = response.xpath("//div[@class='td-pb-span8 td-main-content']//h3[@class='entry-title td-module-title']//a/@href").extract()
        for link in links:
            if self.count<100:
                yield scrapy.Request(link,callback=self.parsePlayer,dont_filter=True)
                self.count+=1
            else:
                break

        next_page = response.xpath("//div[@class='page-nav td-pb-padding-side']//a[last()]//@href").extract()[0]
        if next_page and self.count<100:
            yield scrapy.Request(next_page,callback=self.parse,dont_filter=True)

    def parsePlayer(self,response):
        id = response.url.split('/')[-1]
        name = response.xpath("//div[@class='td-post-content']//p//strong//text()").extract()[0]
        gender = "Male"
        try: 
            heightstring = response.xpath("//p[contains(text(),'cm')]//text()").extract()[0].replace(u'\xa0',u'')
        except:
            heightstring = response.xpath("//p[contains(text(),'in or')]//text()").extract()[0].replace(u'\xa0',u'')
        height = re.findall(r'([\d.]{3,})',heightstring)[-1]
        weightstring = response.xpath("//p[contains(text(),'kg or')]//text()").extract()[0].replace(u'\xa0',u'')
        weight = re.findall(r'(\d{2,})',weightstring)[0]
        url = response.url
        yield {
            'ID':id,
            'Name':name,
            'Gender':gender,
            'Height':height,
            'Weight':weight,
            'URL':url
        }