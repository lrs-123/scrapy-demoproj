#!/usr/bin/env python
# coding:utf-8
"""
-------------------------------------------------------------
    Creator : 汪春旺
       Date : 2018-07-11
    Project : scrapyproj
   FileName : dingdian.py
Description : 
-------------------------------------------------------------
"""
import scrapy
from scrapyproj.items import ScrapyprojItem


class DingDianSpider(scrapy.Spider):
    name = 'dingdian'
    allowed_domains = ['x23us.com']
    leftpart_url = 'http://www.x23us.com/class/'
    rightpart_url = '.html'

    # 可以直接全使用start_urls装入全部请求，不过并不太美观。可以重写start_requests方法
    # 按小说类别分别爬取
    def start_requests(self):
        for i in range(1, 11):
            urls = self.leftpart_url + str(i) + '_1' + self.rightpart_url
            yield scrapy.Request(url=urls, callback=self.parse)

    def parse(self, response):
        dd_items = ScrapyprojItem()
        novels = response.xpath('//div[@class="bdsub"]//dl[@id="content"]//dd//table//tr[position()>1]')
        for item in novels:
            dd_items['name'] = item.xpath('.//td/a[2]/text()').extract_first()
            dd_items['section'] = item.xpath('./td[2]//text()').extract_first()
            dd_items['author'] = item.xpath('./td[3]//text()').extract_first()
            dd_items['words'] = item.xpath('./td[4]//text()').extract_first()
            dd_items['update'] = item.xpath('./td[5]//text()').extract_first()
            dd_items['status'] = item.xpath('./td[6]//text()').extract_first()
            yield dd_items

        # 爬取下一页，数据量大
        # next_page_sl = response.xpath('//div[@id="pagelink"]/a[@class="next"]/@href').extract()
        # if next_page_sl:
        #     next_page = next_page_sl[0]
        #     yield scrapy.Request(url=next_page, callback=self.parse)
