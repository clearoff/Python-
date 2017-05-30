# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ArticlespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class ArticleItem(scrapy.Item):

	title = scrapy.Field()
	pub_time = scrapy.Field()
	article_url = scrapy.Field()
	article_md5_url = scrapy.Field()
	front_image_url = scrapy.Field()
	front_image_path = scrapy.Field()
	collect_num = scrapy.Field()
	like_num = scrapy.Field()
	comment_num = scrapy.Field()
	tags = scrapy.Field()
	content = scrapy.Field()
