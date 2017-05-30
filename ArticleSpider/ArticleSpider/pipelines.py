# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.images import ImagesPipeline
import codecs
import json

class ArticlespiderPipeline(object):
    def process_item(self, item, spider):
        return item

class JsonWithEncodingPipeline(object):
	def __init__(self):
		self.file = codecs.open("article.json","wb",encoding="utf-8")
	
	def process_item(self, item, spider):
		lines = json.dumps(dict(item),ensure_ascii=False)
		lines = lines + '#######################################\n'
		self.file.write(lines)
		return item 

	def spider_closed(self, spider):
		self.file.close()

class ArticleImagePipeline(ImagesPipeline):
	def item_completed(self, results, item, info):
		for ok, value in results:
			image_file_path = value["path"]
		print "image_path:",image_file_path
		item["front_image_path"] = image_file_path
		return item 
