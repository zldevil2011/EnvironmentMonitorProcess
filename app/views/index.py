# coding=utf-8
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from dss.Serializer import serializer
import json


def index(request):
	# 获取所有观测点的数据

	# 对所有的观测点进行数据平均计算AQI／PM2.5／首要污染物
	return render(request, "app/index.html", {

	})