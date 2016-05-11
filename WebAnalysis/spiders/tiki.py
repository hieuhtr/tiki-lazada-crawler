# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from WebAnalysis.items import WebanalysisItem
import re
from datetime import datetime

FILE_PATH = 'tiki_category_links.txt'
date = datetime.now()


def read_list_from_file(path):
    list_of_start_urls = []
    for line in open(path, 'r'):
        list_of_start_urls.append(line.strip())
    return list_of_start_urls

def strip_value(value):
    m = re.search("http[^\s]+(\s)*h?(http[^\s>]+)(\s)*", value)
    if m:
        #print m.group(2).encode('UTF-8')
        return m.group(2)
    else:
        #print value.encode('UTF-8')
        return value

class TikiSpider(CrawlSpider):
    name = 'tiki'
    list_of_start_urls = read_list_from_file(FILE_PATH)

    allowed_domains = ['tiki.vn']
    start_urls = list_of_start_urls

    rules = (
    #    #Rule(LinkExtractor(allow='p[0-9]+', 
    #        #deny=['/customer/', '/sales/', '/order/', '/checkout/', '/nhan-xet', '/tel', '/(\s)+/'],
    #        #process_value=strip_value), callback='parse_item', follow=True, process_links=None),
        Rule(LinkExtractor(allow='\?page=\d+', 
            deny=['/customer/', '/sales/', '/order/', '/checkout/', '/nhan-xet', '/tel', '/\s+/', '/author/', '/TIKI/', '/\w+\.tiki\.vn/', '/hoi-dap/'],
            process_value=strip_value,
            restrict_xpaths=['//div[@class="list-pager"]']), follow=True, process_links=None),
        Rule(LinkExtractor(allow='p\d+', 
            deny=['/customer/', '/sales/', '/order/', '/checkout/', '/nhan-xet', '/tel', '/\s+/', '/author/', '/TIKI/', '/\w+\.tiki\.vn/', '/hoi-dap/'],
            process_value=strip_value,
            restrict_xpaths=['//div[@class="product-box-list"]']), follow=False, callback='parse_item', process_links=None)        
    )

    def parse_item(self, response):
        i = WebanalysisItem()
        try:
            i['product_id'] = response.xpath('//input[@id="product_id"]/@value').extract()[0].strip().encode('UTF-8')
            i['url_product'] = response.url
            i['website'] = 'Tiki'
            i['date'] = '2016-05-15'
        except Exception:
            return

        try:
            i['title'] = response.xpath('//h1[@class="item-name"]/text()').extract()[0].strip().encode('UTF-8')
        except Exception:
            i['title'] = ""

        try:
            if len(response.xpath('//ol[@class="breadcrumb"]/li').extract()) > 2:
                i['category'] = response.xpath('//ol[@class="breadcrumb"]/li[2]/a/text()').extract()[0].strip().encode('UTF-8')
            else:
                i['category'] = ""
        except Exception:
            i['category'] = ""

        try:
            i['current_price'] = int(response.xpath('//p[@class="special-price-item"]/@data-value').extract()[0].strip().encode('UTF-8'))
        except Exception:
            i['current_price'] = 0

        try:
            i['original_price'] = int(response.xpath('//p[@class="old-price-item"]/@data-value').extract()[0].strip().encode('UTF-8'))
        except Exception:
            i['original_price'] = i['current_price']

        

        try:
            description = ""
            block_desc = response.xpath('//div[@id="gioi-thieu"]')
            number_of_desc = len(block_desc.xpath('p').extract())
            for desc in range(1, number_of_desc + 1):
                sub_desc = "".join(block_desc.xpath('p['+str(desc)+']//text()').extract()).encode('UTF-8')
                description += sub_desc + "\n"
            if description:
                i['description'] = description
        except Exception:
            i['description'] = "" 

        try:
            detail_info = {}
            detail_table = response.xpath('//table[@id="chi-tiet"]/tbody')
            number_of_rows = len(detail_table.xpath('tr').extract())
            for row in range(number_of_rows):
                key = detail_table.xpath('tr/td[1]/text()').extract()[row].strip().encode('UTF-8').replace(".","")
                td_value = detail_table.xpath('tr/td[2]')[row]
                try:
                    value = td_value.xpath('a/text()').extract()[0].strip().encode('UTF-8')
                            
                except Exception:
                    value = td_value.xpath('text()').extract()[0].strip().encode('UTF-8')
                finally:
                    detail_info[key] = value
            i['detail_info'] = detail_info
        except Exception:
            i['detail_info'] = ""

        try:
            i['rating'] = response.xpath('//p[@class="total-review-point"]/text()').extract()[0].strip().encode('UTF-8')
        except Exception:
            i['rating'] = ""

        try:
            rating_content = response.xpath('//p[@class="comments-count"]/a/text()').extract()[0].strip().encode('UTF-8')
            number_of_rating = re.search(r'\d+', rating_content)
            i['number_of_rating'] = number_of_rating.group()
        except Exception:
            i['number_of_rating'] = ""

        try:
            list_of_comment = []
            comment_table = response.xpath('//div[@id="review-new"]')
            number_of_comment = len(comment_table.xpath('div').extract())
            for row in range(1, 6 if number_of_comment > 5 else number_of_comment + 1):
                comment = {}
                name = comment_table.xpath('div['+str(row)+']//p[@class="name"]/text()').extract()[0].strip().encode('UTF-8')
                days = comment_table.xpath('div['+str(row)+']//p[@class="days"]/text()').extract()[0].lstrip("(").rstrip(")").encode('UTF-8')
                review = comment_table.xpath('div['+str(row)+']//p[@class="review"]/a/text()').extract()[0].strip().encode('UTF-8')
                review_detail = comment_table.xpath('div['+str(row)+']//span[@class="review_detail"]/text()').extract()[0].strip().encode('UTF-8')
                comment['name'] = name
                comment['days'] = days
                comment['review'] = review
                comment['review_detail'] = review_detail
                list_of_comment.append(comment)
            if list_of_comment:
                i['list_of_comment'] = list_of_comment
        except Exception:
            i['list_of_comment'] = ""


        return i

#        self.logger.info('A response from %s just arrived!', response.url)
