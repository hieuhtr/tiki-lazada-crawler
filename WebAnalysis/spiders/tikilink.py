# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector

import re
import urlparse

FILE_PATH = 'tiki_category_links.txt'

def format_link(url):
	if not url.startswith('http://tiki.vn/'):
		url = urlparse.urljoin('http://tiki.vn/', url)
		# print url
	return url

def append_to_file(path, url):
	with open(path, 'a') as f:
		if url != 'javascript:void(0);':
			f.write(url + "\n")

class TikilinkSpider(scrapy.Spider):
    name = "tikilink"
    allowed_domains = ["tiki.vn"]
    start_urls = (
        'http://tiki.vn/',
    )

    def parse(self, response):
        links = Selector(response).xpath('//nav[@class="header-navigation"]//a/@href')
        for link in links:           
            url = link.extract()
            url = format_link(url)

            append_to_file(FILE_PATH, url)


            

