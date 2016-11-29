# coding=utf-8
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from dss.Serializer import serializer
import json
from app.models import Announcement
from utils.get_news_list import Spider

def information(request):
	# spider = Spider()
	# htmlValue = spider.getHtml()
	# spider.findData(htmlValue)
	file_object = open('test.txt')
	news_data = []
	list_of_all_the_lines = file_object.readlines()
	file_object.close()
	# print list_of_all_the_lines
	idx = 0
	while idx <= (len(list_of_all_the_lines) - 2):
		tmp = {}
		tmp["link"] = list_of_all_the_lines[idx+1]
		tmp["name"] = list_of_all_the_lines[idx]
		news_data.append(tmp)
		idx += 2
	# news_data = spider.data
	# print news_data
	# 本站新闻
	news_list = Announcement.objects.all()
	return render(request, "app/information.html", {
		"news_latest": news_data[0:7],
		"news_policy": news_data[8:17],
		"news_life": news_data[18:],
		"news_list": news_list,
	})


def news_info(request, news_id):
	news_id = int(news_id)
	print news_id
	print type(news_id)
	if request.method == "POST":
		return HttpResponse("POST")
	else:
		try:
			news = Announcement.objects.get(pk=news_id)
			news.read_count += 1
			news.save()
		except Announcement.DoesNotExist:
			return HttpResponse("不存在")

		return render(request, "app/document_info.html", {
			"news": news,
		})