# coding=utf-8
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from dss.Serializer import serializer
import json
from app.forms import AnnouncementUEditorForm, AnnouncementUEditorModelForm
from app.models import Adminer
import math

def admin_data(request):
	try:
		adminer = Adminer.objects.get(username=request.session["username"])
	except:
		return HttpResponseRedirect("/admin_login/")
	page = int(request.GET.get("page", 1))
	if page < 1:
		return HttpResponseRedirect("/admin_data/?page=1")
	start_num = (page - 1) * 30
	end_num = page * 30
	datas_list_all = [
		{"id":"1", "name": u"京师方圆", "so2": 32, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 158,"time": "2016-11-23 12:00:00"},
		{"id":"1", "name": u"京师方圆", "so2": 32, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 158,"time": "2016-11-23 12:00:00"},
		{"id":"1", "name": u"京师方圆", "so2": 32, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 158,"time": "2016-11-23 12:00:00"},
		{"id":"1", "name": u"京师方圆", "so2": 32, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 158,"time": "2016-11-23 12:00:00"},
		{"id":"1", "name": u"京师方圆", "so2": 32, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 158,"time": "2016-11-23 12:00:00"},
		{"id":"1", "name": u"京师方圆", "so2": 32, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 158,"time": "2016-11-23 12:00:00"},
		{"id":"1", "name": u"京师方圆", "so2": 32, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 158,"time": "2016-11-23 12:00:00"},

	]
	data_len = len(datas_list_all)
	total_page = int(math.ceil(data_len/30.0))
	if total_page < 1:
		total_page = 1
	if page > total_page:
		return HttpResponseRedirect("/admin_data/?page=" + str(total_page))
	data = datas_list_all[start_num:end_num]

	device_list = [
		{"id": 1, "name": u"京师方圆", "address": u"凤凰大道", "longitude": 117.2944, "latitude": 30.4127,
		 "latest_time": "2016-11-22 12:00:00", "install_time": "2016-11-12 12:00:00"},
		{"id": 2, "name": u"清风大道路", "address": u"新城区", "longitude": 117.2944, "latitude": 30.4027,
		 "latest_time": "2016-11-22 12:00:00", "install_time": "2016-11-10 12:00:00"},
	]
	return render(request, "admin/admin_data.html", {
		"adminer": adminer,
		"data": data,
		"device_list": device_list,
	})
	# form = ItemUEditorModelForm(instance=item)