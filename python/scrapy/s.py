# -*- coding=utf-8 -*-
import scrapy

class gitspider(scrapy.Spider):
    name = 'sylgit'

    def start_requests(self):
        url_tmpl = 'https://github.com/shiyanlou?page={}&tab=repositories'
        urls = (url_tmpl.format(i) for i in range(1, 5))
        for url in urls:
            print(url)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self,response):
        for res in response.css('li.public'):
            yield{
            'name' : res.xpath('.//a[@itemprop="name codeRepository"]/text()').re_first("\n\s*(.*)"),
            'update_time' : res.xpath('.//relative-time/@datetime').extract_first()
                    }
