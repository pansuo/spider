#!/usr/bin/env python
# -*- coding: utf-8 -*-
# tankywoo@2013-02-21

import urllib2
import threading
from Queue import Queue
from HTMLParser import HTMLParser

url ='http://wiki.wutianqi.com/command/curl.html' 

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

class Spider(threading.Thread):
	def __init__(self, queue, depth=2):
		threading.Thread.__init__(self)
		self.queue = queue
		self.depth = depth
		#self._add_url((1, url))	# root目录是第1层
	
	def _add_url(self, url_node):
		self._fix_url(url_node[1])
		self.queue.put(url_node)

	def _get_url(self):
		return self.queue.get()

	def _fix_url(self, url):
		if url.startswith('/'):
			pass
		if url.endswith('/'):
			pass

	def get_urls(self, url_node):
		_depth, url = url_node		
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
			if _depth == self.depth:
				return
			try:
				parser = Parser()
				parser.feed(html)
			except:
				print 'unknown error'
			#print parser.urls
			for url in parser.urls:
				self._add_url((_depth+1, url))

	def run(self):
		print 'run function'
		while not self.queue.empty():
			url_node = self._get_url()
			self.get_urls(url_node)
			self.queue.task_done()
		print 'end'

def Work():
	queue = Queue()
	for i in xrange(3):
		r = Spider(queue)
		r.setDaemon(True)
		r.start()
	queue.put((1, url))
	queue.join()

if __name__ == '__main__':
	#myspider = Spider(url)
	#myspider.run()
	Work()
