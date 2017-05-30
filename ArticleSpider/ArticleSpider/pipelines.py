# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES settings
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.images import ImagesPipeline
import codecs
import json
from scrapy.exporters import JsonItemExporter 
from twisted.enterprise import adbapi
import MySQLdb
import MySQLdb.cursors

class ArticlespiderPipeline(object):
    def process_item(self, item, spider):
        return item

class MysqlSynPipeline(object):
	def __init__(self, dbpool):
		self.dbpool = dbpool

	@classmethod
	def from_settings(cls, settings):
		dbparms = dict(host = settings["MYSQL_HOST"],
				db = settings["MYSQL_DBNAME"],
				user = settings["MYSQL_USER"],
				passwd = settings["MYSQL_PASSWD"],
				charset = 'utf8',
				cursorclass=MySQLdb.cursors.DictCursor,
				use_unicode = True,
		)
		print "############################################"
		print dbparms["db"],dbparms["user"],dbparms["passwd"],dbparms["host"]
		print "############################################"
		dbpool = adbapi.ConnectionPool("MySQLdb",**dbparms)
		return cls(dbpool)

	def process_item(self,item,spider):
		query = self.dbpool.runInteraction(self.do_insert, item)
		query.addErrback(self.handle_error) #处理异常
	
	def handle_error(self, failure):
		print (failure)

	def do_insert(self, cursor, item):


		insert_sql = """
			insert into article_msg(url_object_id, article_name, url, pub_time, praise_num, tags, comment_num, collect_num, content, front_image_url, front_image_path)
			values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
		"""
		cursor.execute(insert_sql,(item["article_md5_url"],\
				item["title"], item["article_url"], item["pub_time"],\
				item["like_num"], item["tags"], item["comment_num"],\
				item["collect_num"], item["content"], item["front_image_url"], item["front_image_path"]))
		#insert_sql, params = item.get_insert_sql()
		##print "sql : ",insert_sql 
		##print "parms :",params
		#cursor.execute(insert_sql, params)

	

class MysqlPipeline(object):
	def __init__(self):
		self.conn = MySQLdb.connect(\
				'0.0.0.0',\
				'root',\
				'960324',\
				'spider',\
				charset="utf8",\
				use_unicode=True
				)
		self.cursor = self.conn.cursor()

	def process_item(self, item, spider):
		insert_sql = """
			insert into article_msg(url_object_id, article_name, url, pub_time, praise_num, tags)
			values (%s, %s, %s, %s, %s, %s)
		"""
		self.cursor.execute(insert_sql,(item["article_md5_url"],\
				item["title"], item["article_url"], item["pub_time"],\
				item["like_num"], item["tags"]))
		self.conn.commit()
		return item 


class JsonExporterPipeline(object):
	def __init__(self):
		self.file = open("articleexport.json","wb")
		self.exporter = JsonItemExporter(self.file, \
				encoding='utf-8',ensure_ascii=False)
		self.exporter.start_exporting()

	def close_spider(self, spider):
		self.exporter.finish_exporting()
		self.file.close()
	
	def process_item(self,item,spider):
		self.exporter.export_item(item)
		return item 

class JsonWithEncodingPipeline(object):
	def __init__(self):
		self.file = codecs.open("article.json","wb",encoding="utf-8")
	
	def process_item(self, item, spider):
		print "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
		print item["title"]
		print item["pub_time"]
		print item["article_url"]
		print item["article_md5_url"]
		#lines = json.dumps(dict(item),ensure_ascii=False)
		#lines = lines + '#######################################\n'
		#self.file.write(lines)
		return item 

	def spider_closed(self, spider):
		self.file.close()

class ArticleImagePipeline(ImagesPipeline):
	def item_completed(self, results, item, info):
		if "front_image_url" in item:
			for ok, value in results:
				image_file_path = value["path"]
			item["front_image_path"] = image_file_path
		return item 
