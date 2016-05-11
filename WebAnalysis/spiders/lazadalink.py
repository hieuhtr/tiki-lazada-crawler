# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector

import re
import urlparse

FILE_PATH = 'lazada_category_links.txt'

def format_link(url):
	if not url.startswith('http://lazada.vn/'):
		url = urlparse.urljoin('http://lazada.vn/', url)
		# print url
	return url

def append_to_file(path, url):
	with open(path, 'a') as f:
		if url != 'javascript:void(0);':
			f.write(url + "\n")

class LazadalinkSpider(scrapy.Spider):
    name = "lazadalink"
    allowed_domains = ["www.lazada.vn"]
    start_urls = (
        'http://www.lazada.vn/',
    )

    def parse(self, response):
        links = Selector(response).xpath('//div[@class="sidebarSecond__wrapper"]//a/@href')
        for link in links:           
            url = link.extract()
            url = format_link(url)

            append_to_file(FILE_PATH, url)
