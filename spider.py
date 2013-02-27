#!/usr/bin/env python
# -*- coding: utf-8 -*-
# tankywoo@2013-02-21

# @todo
# 增加logging
# 增加线程池

import urllib2
from HTMLParser import HTMLParser

from threadpool import ThreadPool

import time

url ='http://www.sina.com.cn/' 

user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
header = {'User-Agent':user_agent}

class Parser(HTMLParser):
	def reset(self):
		self.urls = []	# ???
		HTMLParser.reset(self)

	def handle_starttag(self, tag, attrs):
		href = [v for k,v in attrs if k=='href']
		if href:
			self.urls.extend(href)

class Spider:
	def __init__(self, depth=30):
		self.threadPool = ThreadPool(5)
		self.depth = depth

	def start(self, url):
		self.threadPool.initPool()
		self.threadPool.putTask(self.get_urls, url)

	def get_urls(self, url):
		req = urllib2.Request(url=url, headers=header)
		try:
			resp = urllib2.urlopen(req, timeout=10)
		except urllib2.HTTPError as e:
			# XXX The except HTTPError must come first
			# otherwise except URLError will also catch an HTTPError
			print '>> The server %s counldn\'t filfill the request' % url
			print 'Error code:', e.code
		except urllib2.URLError as e:
			print '>> We failed to reach %s' % url
			print 'Reason:', e.reason
		except Exception, e:
			print e
		else:
			print resp.geturl()
			html = resp.read()
			try:
				parser = Parser()
				parser.feed(html)
			except:
				print 'unknown error'
			for url in parser.urls:
				if url.startswith('http:'):
					self.threadPool.putTask(self.get_urls, url)


if __name__ == '__main__':
	spider = Spider()
	spider.start(url)
