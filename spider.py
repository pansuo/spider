#!/usr/bin/env python
# -*- coding: utf-8 -*-
# tankywoo@2013-02-21

# @todo
# 增加logging
# FIXME 如果总任务小于threadNum，则无法达到task_done()数，而不停止

import urllib2
from HTMLParser import HTMLParser

from threadpool import ThreadPool

import time

#url ='http://www.sina.com.cn/' 
#url ='http://www.douban.com/'
url ='http://www.baidu.com/'

user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
header = {'User-Agent':user_agent}

class Parser(HTMLParser):
	# TODO 可以换bs4
	def reset(self):
		self.urls = []	# ???
		HTMLParser.reset(self)

	def handle_starttag(self, tag, attrs):
		href = [v for k,v in attrs if k=='href']
		if href:
			self.urls.extend(href)

class Spider:
	def __init__(self, depth=2):
		self.threadPool = ThreadPool(10)
		self.depth = depth

	def start(self, currentLevel, url):
		self.threadPool.initPool()
		self.threadPool.putTask(self.crawlPage, \
							currentLevel = currentLevel, \
							url = url)

	def crawlPage(self, args):
		print 'crawlPage', args
		currentLevel = args['currentLevel']
		url = args['url']
		req = urllib2.Request(url=url, headers=header)
		try:
			resp = urllib2.urlopen(req, timeout=10)
		except urllib2.HTTPError as e:
			# XXX The except HTTPError must come first
			# otherwise except URLError will also catch an HTTPError
			pass
		except urllib2.URLError as e:
			pass
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
			
			if currentLevel < self.depth:
				pass
			elif currentLevel == self.depth:
				return
			else:
				pass	# TODO ERROR

			for url in parser.urls:
				# TODO
				if url.startswith('http:'):
					self.threadPool.putTask(self.crawlPage, \
							currentLevel = currentLevel+1, \
							url = url)

	def stop(self):
		self.threadPool.stopPool()

if __name__ == '__main__':
	spider = Spider()
	spider.start(1, url)
	spider.stop()
