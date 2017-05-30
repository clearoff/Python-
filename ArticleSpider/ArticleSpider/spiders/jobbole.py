# -*- coding: utf-8 -*-
import scrapy
import re 
from scrapy.http import Request
import urlparse 
import datetime
import sys
from  ArticleSpider.items import ArticleItem
from  ArticleSpider.comm import get_md5

reload(sys)
sys.setdefaultencoding('utf8')

class JobboleSpider(scrapy.Spider):
	name = "jobbole"
	allowed_domains = ["blog.jobbole.com"]
	start_urls = ["http://blog.jobbole.com/all-posts/"]

	def parse(self, response):
		post_nodes = response.css("#archive .floated-thumb .post-thumb a")
		for post_node in post_nodes:
			image_url = post_node.css("img::attr(src)").extract_first("") 
			post_url = post_node.css("::attr(href)").extract_first("")
			#print "post_url:",urlparse.urljoin(response.url,post_url)
			yield Request(url=urlparse.urljoin(response.url, post_url),\
					meta={"front_image_url":image_url} ,\
					callback=self.parse_info)
		pass

	def parse_info(self, response):
		article_item = ArticleItem()
		print u"-------------------------------------------------"
		front_image_url = response.meta.get("front_image_url","")
		title = response.css(".entry-header h1::text").extract()[0]
		pubtime = response.css("p.entry-meta-hide-on-mobile::text").extract()[0].strip().replace("·","").strip()
		like_num = response.css(".vote-post-up h10::text").extract()[0]
		collect_num = response.css(".bookmark-btn::text").extract()[0]
		match_re = re.match(".*?(\d+).*?",collect_num)
		if match_re:
			collect_num = match_re.group(1)
		else:
			collect_num = 0
		comment_num = response.css('.post-adds a[href="#article-comment"] .btn-bluet-bigger::text ').extract()[0].strip()
		match_re = re.match(".*?(\d+).*?",comment_num)
		if match_re:
			comment_num = match_re.group(0)
		else:
			comment_num = 0
		tag_list = response.css("p.entry-meta-hide-on-mobile a::text").extract()
		tag_list = [element for element in tag_list if not element.strip().endswith("评论")]
		tags = ",".join(tag_list)
		article_item['title'] = title 
		article_item['front_image_url'] = [front_image_url] 
		article_item['article_md5_url'] = get_md5(response.url)
		try:
			pubtime = datetime.datetime.strptime(create_date, "%Y/%m/%d").date()
		except Exception as e:
			pubtime = datetime.datetime.now().date()
		article_item['pub_time'] = pubtime
		article_item['article_url'] = response.url
		article_item['like_num'] = like_num
		article_item['collect_num'] = collect_num 
		article_item['comment_num'] = comment_num
		article_item['tags'] = tags 
		article_item['content'] = response.css('div.entry ')\
				.extract_first("")
		print u"crawled ",response.url
		#print "title:",title 
		#print "image:",front_image_url
		#print "pubtime:",pubtime 
		#print "likes:",like_num
		#print "collects:",collect_num
		#print "comments:",comment_num
		#print "tags:",tags
		print u"-------------------------------------------------"
		yield article_item
