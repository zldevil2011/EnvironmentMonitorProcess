# -*- coding:utf-8 -*-
import re
import urllib2
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class Spider(object):
	def __init__(self):
		self.my_url = "http://www.pm25.com/news.html"
		self.data = []
		self.reg_list = []
		self.reg_list.append(u'<li><a href="http://www.pm25.com/news(.*?)".*?><i>•</i>(.*?)</a></li>')

	def getHtml(self):
		url = self.my_url
		headers = {
			'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
		}
		req = urllib2.Request(url=url, headers=headers)
		print url
		try:
			htmlValue = urllib2.urlopen(req).read().decode('utf-8')
		except Exception, e:
			print "faild to get the value in page code " + str(e)
			return ""
		# print htmlValue
		return htmlValue

	def findData(self, htmlValue):
		print "XXXXXXXXXX"
		data_items = re.findall(self.reg_list[0], htmlValue, re.S)
		# print data_items
		# fileHandle = open('test.txt', 'w')
		for item in data_items:
			tmp = {}
			tmp["name"] = str(item[1])
			tmp["link"] = 'http://www.pm25.com/news' + str(item[0])
			self.data.append(tmp)
			# fileHandle.write(str(item[1]) + '\n')
			# fileHandle.write('http://www.pm25.com/news' + str(item[0]) + '\n')
		print len(self.data)
		# fileHandle.close()


def main():
	spider = Spider()
	htmlValue = spider.getHtml()
	spider.findData(htmlValue)


if __name__ == '__main__':
	main()
