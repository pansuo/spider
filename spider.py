#!/usr/bin/env python
# -*- coding: utf-8 -*-
# wutq@2013-02-21

import urllib2

url ='http://tankywoo.com' 

user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
header = {'User-Agent':user_agent}


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
	#print html
	print 'end...'
