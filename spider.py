#!/usr/bin/env python
# -*- coding: utf-8 -*-
# tankywoo@2013-02-21

import urllib2
from HTMLParser import HTMLParser

url ='http://wiki.wutianqi.com/command/curl.html' 

user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
header = {'User-Agent':user_agent}

class Parser(HTMLParser):
	def reset(self):
		self.urls = []
		HTMLParser.reset(self)
	def handle_starttag(self, tag, attrs):
		href = [v for k,v in attrs if k=='href']
		if href:
			self.urls.extend(href)

req = urllib2.Request(url=url, headers=header)
try:
	resp = urllib2.urlopen(req, timeout=10)
except urllib2.HTTPError as e:
	# XXX The except HTTPError must come first
	# otherwise except URLError will also catch an HTTPError
	print 'The server counldn\'t filfill the request'
	print 'Error code:', e.code
except urllib2.URLError as e:
	print 'We failed to reach a server'
	print 'Reason:', e.reason
else:
	html = resp.read()
	parser = Parser()
	parser.feed(html)
	print parser.urls
	print 'end...'
