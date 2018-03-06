# -*- coding: utf-8 -*-
import scrapy
from shiyanlougithub.items import ShiyanlougithubItem 


class RepositoriesSpider(scrapy.Spider):
    name = 'repositories'
    
    @property
    def start_urls(self):
        url = 'https://github.com/shiyanlou?page={}&tab=repositories'
        return (url.format(i) for i in range(1,5))

    def parse(self, response):
        for res in response.css('li.public'):
            item = ShiyanlougithubItem({
                 'name' : res.xpath('.//a[@itemprop="name codeRepository"]/text()').re_first("\n\s*(.*)"),
                 'update_time' : res.xpath('.//relative-time/@datetime').extract_first()
            })
            yield item

