# coding=utf-8
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from dss.Serializer import serializer
import json
from utils.get_news_list import Spider

def information(request):
	spider = Spider()
	htmlValue = spider.getHtml()
	spider.findData(htmlValue)
	news_data = spider.data
	print news_data
	return render(request, "app/information.html", {
		"news_latest": news_data[0:7],
		"news_policy": news_data[8:17],
		"news_life": news_data[18:],
	})