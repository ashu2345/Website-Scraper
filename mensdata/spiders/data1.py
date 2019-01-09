# -*- coding: utf-8 -*-
import scrapy
import csv


class Data1Spider(scrapy.Spider):
    name = 'data1'
    allowed_domains = ['healthyceleb.com/']
    start_urls = ['https://healthyceleb.com/category/statistics/sports-stars/female-sports-stars/']
    count = 0

    def parse(self, response):
        links = response.xpath("//div[@class='td-pb-span8 td-main-content']//h3[@class='entry-title td-module-title']//a/@href").extract()
        for link in links:
            if self.count<100:
                yield scrapy.Request(link,callback=self.parsePlayer,dont_filter=True)
            else:
                break

        next_page = response.xpath("//div[@class='page-nav td-pb-padding-side']//a[last()]//@href").extract()[0]
        if next_page and self.count<100:
            yield scrapy.Request(next_page,callback=self.parse,dont_filter=True)

    def parsePlayer(self,response):
        id = response.url.split('/')[-1]
        name = response.xpath("//div[@class='td-post-content']//p//strong//text()").extract()[0]
        gender = "Female"
        height = response.xpath("//p[contains(text(),'cm')]//text()").extract()[0].split(' ')[-2]
        weight = response.xpath("//p[contains(text(),'kg or')]//text()").extract()[0].split(' ')[-2]
        url = response.url
        self.count+=1
        yield {
            'ID':id,
            'Name':name,
            'Gender':gender,
            'Height':height,
            'Weight':weight,
            'URL':url
        }