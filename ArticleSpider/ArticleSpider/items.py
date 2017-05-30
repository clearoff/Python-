# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import re
from scrapy.loader.processors import MapCompose, Join, TakeFirst
from scrapy.loader import ItemLoader
import datetime


class ArticlespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


def add_title(title):
	return title + '-jobbole'


def get_time(value):
	try:
		pubtime = datetime.datetime.strptime(value, "%Y/%m/%d").date()
	except Exception as e:
		pubtime = datetime.datetime.now().date()
	return pubtime


def return_value(value):
	return value


def get_nums(value):
	match_re = re.match(".*?(\d+).*?", value)
	if match_re:
		nums = int(match_re.group(1))
	else:
		nums = 0
	return nums


def remove_comment_tags(value):
	if "评论" in value:
		return ""
	else:
		return value


class ArticleItemLoader(ItemLoader):
	default_output_processor = TakeFirst()


class ArticleItem(scrapy.Item):

	# setting parm item
	title = scrapy.Field(
		input_processor = MapCompose(add_title)
	)
	pub_time = scrapy.Field(
		input_processor = MapCompose(get_time),		
		output_processor = TakeFirst()
	)
	article_url = scrapy.Field()
	article_md5_url = scrapy.Field()
	front_image_url = scrapy.Field(
		output_processor = MapCompose(return_value)		
	)
	front_image_path = scrapy.Field()
	collect_num = scrapy.Field(
		input_processor = MapCompose(get_nums)		
	)
	like_num = scrapy.Field(
		input_processor = MapCompose(get_nums)		
	)
	comment_num = scrapy.Field(
		input_processor = MapCompose(get_nums)		
	)
	tags = scrapy.Field(
		input_processor = MapCompose(remove_comment_tags),
		output_processor = Join(",")
	)
	content = scrapy.Field()
