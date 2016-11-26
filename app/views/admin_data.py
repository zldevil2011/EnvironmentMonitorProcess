# coding=utf-8
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from dss.Serializer import serializer
import json
from app.forms import AnnouncementUEditorForm, AnnouncementUEditorModelForm
from app.models import Adminer
import math
from utils.mySqlUtils import MySQL

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

	sql = MySQL()
	sql.connectDB("projectmanagement")
	devices = sql.get_query("projectnodeinfo", "ProjectID", "=", "1")
	sql.close_connect()
	device_list = []
	for device in devices:
		tmp = {}
		tmp["id"] = device["NodeNO"]
		tmp["name"] = device["Description"]
		tmp["address"] = device["InstallationAddress"]
		tmp["longitude"] = "117.5436320000"
		tmp["latitude"] = "30.7078830000"
		tmp["install_time"] = device["SetTime"]
		device_list.append(tmp)
	devices = device_list
	# 连接数据库，获取所有的采集数据
	sql.connectDB("jssf")
	datas = sql.get_query(u"大气六参数")
	sql.close_connect()
	datas_list_briage = []
	for data in datas:
		tmp = {}
		tmp["so2"] = data["SO2_SO2"]
		tmp["no2"] = data["NO2_NO2"]
		tmp["pm10"] = data["PM10_PM10"]
		tmp["co"] = data["CO_CO"]
		tmp["o3"] = data["O3_O3"]
		tmp["pm25"] = data["PM2.5_PM2.5"]
		tmp["device_id"] = data[u"项目内节点编号"]
		tmp["time"] = str(data[u"紧缩型时间传感器_实时时间"])
		datas_list_briage.append(tmp)
	datas = datas_list_briage


	for device in devices:
		for data in datas:
			if device["id"] == data["device_id"]:
				device["latest_time"] = data["time"]
				break
	for data in datas:
		for device in devices:
			if data["device_id"] == device["id"]:
				data["name"] = device["name"]
				break
	print "--------------------------"
	datas_list_all = [
		{"id":"1", "name": u"京师方圆", "so2": 32, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 158,"time": "2016-11-23 12:00:00"},
		{"id":"2", "name": u"京师方圆", "so2": 32, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 158,"time": "2016-11-23 12:00:00"},
		{"id":"3", "name": u"京师方圆", "so2": 32, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 158,"time": "2016-11-23 12:00:00"},
		{"id":"4", "name": u"京师方圆", "so2": 32, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 158,"time": "2016-11-23 12:00:00"},
		{"id":"5", "name": u"京师方圆", "so2": 32, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 158,"time": "2016-11-23 12:00:00"},
		{"id":"6", "name": u"京师方圆", "so2": 32, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 158,"time": "2016-11-23 12:00:00"},
		{"id":"7", "name": u"京师方圆", "so2": 32, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 158,"time": "2016-11-23 12:00:00"},

	]
	datas_list_all = datas
	# print datas
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
	device_list = devices
	return render(request, "admin/admin_data.html", {
		"adminer": adminer,
		"data": data,
		"device_list": device_list,
		"page":page,
		"total_page":total_page,
	})
	# form = ItemUEditorModelForm(instance=item)


@csrf_exempt
def admin_data_update(request):
	try:
		adminer = Adminer.objects.get(username=request.session["username"])
	except:
		return HttpResponseRedirect("/admin_login/")
	try:
		data_id = int(request.POST.get("data_id"))
	except:
		return HttpResponse("error")
	delete_tag = request.POST.get("delete_tag", None)
	pm25 = request.POST.get("pm25", None)
	pm10 = request.POST.get("pm10", None)
	so2 = request.POST.get("so2", None)
	co = request.POST.get("co", None)
	no2 = request.POST.get("no2", None)
	o3 = request.POST.get("o3", None)
	time = request.POST.get("time", None)
	if delete_tag is None:
		data = {}
		data["pm25"] = pm25
		data["pm10"] = pm10
		data["so2"] = so2
		data["co"] = co
		data["no2"] = no2
		data["o3"] = o3
		data["time"] = time
		return HttpResponse("success")
	else:
		return HttpResponse("success")


@csrf_exempt
def admin_device_update(request):
	try:
		adminer = Adminer.objects.get(username=request.session["username"])
	except:
		return HttpResponseRedirect("/admin_login/")
	try:
		device_id = int(request.POST.get("device_id"))
	except:
		return HttpResponse("error")
	delete_tag = request.POST.get("delete_tag", None)
	name = request.POST.get("name", None)
	address = request.POST.get("address", None)
	install_time = request.POST.get("install_time", None)
	if delete_tag is None:
		data = {}
		data["name"] = name
		data["address"] = address
		data["install_time"] = install_time
		return HttpResponse("success")
	else:
		return HttpResponse("success")

