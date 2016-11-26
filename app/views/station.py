# coding=utf-8
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from dss.Serializer import serializer
import json
from objects.AqiParameter import AqiParameter
from datetime import datetime, timedelta
import time
from utils.mySqlUtils import MySQL

def station(request):
	# sql = MySQL()
	# sql.connectDB()
	# datas = sql.get_query("data")
	# devices = sql.get_query("device")
	# sql.close_connect()
	# 连接数据库，获取设备列表
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
	datas = sql.get_query(u"大气六参数", None, None, None, None, u"紧缩型时间传感器_实时时间")
	datas.reverse()
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
				device["install_time"] = device["install_time"]
				break
	for data in datas:
		for device in devices:
			if data["device_id"] == device["id"]:
				data["name"] = device["name"]
				data["time"] = str(data["time"])
				break
	# 计算站点观测情况排行
	# 实时排行，昨日排行，一周排行，一月排行
	datas_list_all = [
		{"name": u"京师方圆", "so2": 32, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 158,
		 "time": "2016-11-22 12:00:00"},
		{"name": u"京师方圆", "so2": 32, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 158,
		 "time": "2016-11-22 12:10:00"},
		{"name": u"京师方圆", "so2": 32, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 158,
		 "time": "2016-11-22 12:20:00"},
		{"name": u"京师方圆", "so2": 32, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 158,
		 "time": "2016-11-22 12:30:00"},
		{"name": u"京师方圆", "so2": 32, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 158,
		 "time": "2016-11-22 12:40:00"},
		{"name": u"京师方圆", "so2": 32, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 158,
		 "time": "2016-11-22 11:00:00"},
		{"name": u"京师方圆", "so2": 32, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 158,
		 "time": "2016-11-22 11:57:00"},
		{"name": u"京师方圆", "so2": 32, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 158,
		 "time": "2016-11-22 11:13:00"},
		{"name": u"京师方圆", "so2": 32, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 158,
		 "time": "2016-11-22 11:35:00"},
		{"name": u"京师方圆", "so2": 32, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 158,
		 "time": "2016-11-22 10:57:00"},
		{"name": u"京师方圆", "so2": 32, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 158,
		 "time": "2016-11-22 10:13:00"},
		{"name": u"京师方圆", "so2": 32, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 158,
		 "time": "2016-11-22 10:35:00"},
		{"name": u"清风大道路", "so2": 32, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 158,
		 "time": "2016-11-22 12:00:00"},
		{"name": u"清风大道路", "so2": 32, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 158,
		 "time": "2016-11-22 12:10:00"},
		{"name": u"清风大道路", "so2": 32, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 158,
		 "time": "2016-11-22 12:20:00"},
		{"name": u"清风大道路", "so2": 32, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 158,
		 "time": "2016-11-22 12:30:00"},
		{"name": u"清风大道路", "so2": 32, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 158,
		 "time": "2016-11-22 12:40:00"},
		{"name": u"清风大道路", "so2": 32, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 158,
		 "time": "2016-11-22 11:00:00"},
		{"name": u"清风大道路", "so2": 32, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 158,
		 "time": "2016-11-22 11:57:00"},
		{"name": u"清风大道路", "so2": 32, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 158,
		 "time": "2016-11-22 11:13:00"},
		{"name": u"清风大道路", "so2": 32, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 158,
		 "time": "2016-11-22 11:35:00"},
		{"name": u"清风大道路", "so2": 32, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 158,
		 "time": "2016-11-22 10:57:00"},
		{"name": u"清风大道路", "so2": 32, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 158,
		 "time": "2016-11-22 10:13:00"},
		{"name": u"清风大道路", "so2": 32, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 158,
		 "time": "2016-11-22 10:35:00"},
	]
	datas_list_all = datas
	# 设备列表
	device_list = [
		{"id": 1, "name": u"京师方圆", "address": u"凤凰大道", "longitude": 117.2944, "latitude": 30.4127, "install_time": "2016-11-12 12:00:00"},
		{"id": 2, "name": u"清风大道路", "address": u"新城区", "longitude": 117.2944, "latitude": 30.4027, "install_time": "2016-11-10 12:00:00"},
	]
	device_list = devices
	# 实时排行
	time_now = datetime.today()
	start_time = datetime(time_now.year, time_now.month, time_now.day, 0, 0, 0)
	end_time = start_time + timedelta(days=1)
	real_time = []
	for device in device_list:
		device_info = {}
		for data in datas_list_all:
			time = datetime.strptime(data["time"], "%Y-%m-%d %H:%M:%S")
			if data["name"] == device["name"] and start_time <= time < end_time:
				cal = AqiParameter()
				cal.get_1_aqi(data)
				device_info["level"] = cal.AQI_info_1["level_no"]
				device_info["name"] = device["name"]
				device_info["AQI"] = cal.AQI_1
				device_info["classification"] = cal.AQI_info_1["classification"]
				device_info["pm25"] = data["pm25"]
				real_time.append(device_info)
				break
	# 昨日排行
	yesterday_time = []
	time_now = datetime.today()
	start_time = datetime(time_now.year, time_now.month, time_now.day, 0,0,0) - timedelta(days=1)
	end_time = start_time + timedelta(days=1)
	for device in device_list:
		data_tmp = {"so2":0, "no2":0, "pm10":0, "co":0, "o3":0, "pm25":0}
		cnt = 0
		for data in datas_list_all:
			time = datetime.strptime(data["time"], "%Y-%m-%d %H:%M:%S")
			if start_time <= time < end_time and data["name"] == device["name"]:
				data_tmp["so2"] += data["so2"]
				data_tmp["no2"] += data["no2"]
				data_tmp["pm10"] += data["pm10"]
				data_tmp["co"] += data["co"]
				data_tmp["o3"] += data["o3"]
				data_tmp["pm25"] += data["pm25"]
				cnt += 1
		if cnt != 0:
			print "cnt=", cnt
			data_tmp["so2"] = (data_tmp["so2"] * 1.0) / cnt
			data_tmp["no2"] = (data_tmp["no2"] * 1.0) / cnt
			data_tmp["pm10"] = (data_tmp["pm10"] * 1.0) / cnt
			data_tmp["co"] = (data_tmp["co"] * 1.0) / cnt
			data_tmp["o3"] = (data_tmp["o3"] * 1.0) / cnt
			data_tmp["pm25"] = (data_tmp["pm25"] * 1.0) / cnt
			cal = AqiParameter()
			cal.get_24_aqi(data_tmp)
			device_info = {}
			print cal
			device_info["level"] = cal.AQI_info_24["level_no"]
			device_info["name"] = device["name"]
			device_info["AQI"] = cal.AQI_24
			device_info["classification"] = cal.AQI_info_24["classification"]
			device_info["pm25"] = round(data_tmp["pm25"], 2)
			yesterday_time.append(device_info)
		else:
			data_tmp["so2"] = u"无数据"
			data_tmp["no2"] = u"无数据"
			data_tmp["pm10"] = u"无数据"
			data_tmp["co"] = u"无数据"
			data_tmp["o3"] = u"无数据"
			data_tmp["pm25"] = u"无数据"


	# 一周排行
	week_time = []
	time_now = datetime.today()
	start_time = datetime(time_now.year, time_now.month, time_now.day, 0, 0, 0) - timedelta(days=7)
	end_time = start_time + timedelta(days=7)
	for device in device_list:
		aqi = 0
		data_tmp = {"so2": 0, "no2": 0, "pm10": 0, "co": 0, "o3": 0, "pm25": 0}
		cnt = 0
		for data in datas_list_all:
			time = datetime.strptime(data["time"], "%Y-%m-%d %H:%M:%S")
			if start_time <= time < end_time and data["name"] == device["name"]:
				data_tmp["so2"] += data["so2"]
				data_tmp["no2"] += data["no2"]
				data_tmp["pm10"] += data["pm10"]
				data_tmp["co"] += data["co"]
				data_tmp["o3"] += data["o3"]
				data_tmp["pm25"] += data["pm25"]
				cnt += 1
		if cnt != 0:
			data_tmp["so2"] = (data_tmp["so2"] * 1.0) / cnt
			data_tmp["no2"] = (data_tmp["no2"] * 1.0) / cnt
			data_tmp["pm10"] = (data_tmp["pm10"] * 1.0) / cnt
			data_tmp["co"] = (data_tmp["co"] * 1.0) / cnt
			data_tmp["o3"] = (data_tmp["o3"] * 1.0) / cnt
			data_tmp["pm25"] = (data_tmp["pm25"] * 1.0) / cnt
			cal = AqiParameter()
			cal.get_24_aqi(data_tmp)
			device_info = {}
			device_info["level"] = cal.AQI_info_24["level_no"]
			device_info["name"] = device["name"]
			device_info["AQI"] = cal.AQI_24
			device_info["classification"] = cal.AQI_info_24["classification"]
			device_info["pm25"] = round(data_tmp["pm25"], 2)
			week_time.append(device_info)
		else:
			data_tmp["so2"] = u"无数据"
			data_tmp["no2"] = u"无数据"
			data_tmp["pm10"] = u"无数据"
			data_tmp["co"] = u"无数据"
			data_tmp["o3"] = u"无数据"
			data_tmp["pm25"] = u"无数据"

	# 一月排行
	month_time = []
	time_now = datetime.today()
	start_time = datetime(time_now.year, time_now.month, time_now.day, 0, 0, 0) - timedelta(days=31)
	end_time = start_time + timedelta(days=31)
	for device in device_list:
		aqi = 0
		data_tmp = {"so2": 0, "no2": 0, "pm10": 0, "co": 0, "o3": 0, "pm25": 0}
		cnt = 0
		for data in datas_list_all:
			time = datetime.strptime(data["time"], "%Y-%m-%d %H:%M:%S")
			if start_time <= time < end_time and data["name"] == device["name"]:
				data_tmp["so2"] += data["so2"]
				data_tmp["no2"] += data["no2"]
				data_tmp["pm10"] += data["pm10"]
				data_tmp["co"] += data["co"]
				data_tmp["o3"] += data["o3"]
				data_tmp["pm25"] += data["pm25"]
				cnt += 1
		if cnt != 0:
			data_tmp["so2"] = (data_tmp["so2"] * 1.0) / cnt
			data_tmp["no2"] = (data_tmp["no2"] * 1.0) / cnt
			data_tmp["pm10"] = (data_tmp["pm10"] * 1.0) / cnt
			data_tmp["co"] = (data_tmp["co"] * 1.0) / cnt
			data_tmp["o3"] = (data_tmp["o3"] * 1.0) / cnt
			data_tmp["pm25"] = (data_tmp["pm25"] * 1.0) / cnt
			cal = AqiParameter()
			cal.get_24_aqi(data_tmp)
			device_info = {}
			device_info["level"] = cal.AQI_info_24["level_no"]
			device_info["name"] = device["name"]
			device_info["AQI"] = cal.AQI_24
			device_info["classification"] = cal.AQI_info_24["classification"]
			device_info["pm25"] = round(data_tmp["pm25"], 2)
			month_time.append(device_info)
		else:
			data_tmp["so2"] = u"无数据"
			data_tmp["no2"] = u"无数据"
			data_tmp["pm10"] = u"无数据"
			data_tmp["co"] = u"无数据"
			data_tmp["o3"] = u"无数据"
			data_tmp["pm25"] = u"无数据"

	return render(request, "app/stations.html", {
		"real_time":real_time,
		"yesterday_time":yesterday_time,
		"week_time":week_time,
		"month_time":month_time,
	})