# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WebanalysisItem(scrapy.Item):
	website = scrapy.Field()
	date = scrapy.Field()
	product_id = scrapy.Field()
	title = scrapy.Field()
	original_price = scrapy.Field()
	current_price = scrapy.Field()
	detail_info = scrapy.Field()
	rating = scrapy.Field()
	number_of_rating = scrapy.Field()
	number_of_comment = scrapy.Field()
	list_of_comment = scrapy.Field()
	description = scrapy.Field()
	url_product = scrapy.Field()
	category = scrapy.Field()