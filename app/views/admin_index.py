# coding=utf-8
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from dss.Serializer import serializer
import json
from app.forms import AnnouncementUEditorForm, AnnouncementUEditorModelForm
from app.models import Adminer
from objects.AqiParameter import AqiParameter
from datetime import datetime, timedelta
from utils.mySqlUtils import MySQL
transform_factor = {"so2": 2949.276785714286, "o3": 2142.7767857142856, "co": 1.2504464285714287, "no2": 2054.017857142857}

def admin_index(request):
	try:
		adminer = Adminer.objects.get(username=request.session["username"])
	except:
		return HttpResponseRedirect("/admin_login/")
	sql = MySQL()
	sql.connectDB("projectmanagement")
	data = {}
	data["ProjectID"] = {}
	data["ProjectID"]["conn"] = "="
	data["ProjectID"]["val"] = str(1)
	devices = sql.get_query("projectnodeinfo", data)
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
	NOW = datetime.today()
	start = datetime(NOW.year, NOW.month, NOW.day, 0,0,0)
	sql.connectDB("jssf")
	data = {}
	data["紧缩型时间传感器_实时时间"] = {}
	data["紧缩型时间传感器_实时时间"]["conn"] = ">"
	data["紧缩型时间传感器_实时时间"]["val"] = start.strftime("%Y-%m-%d %H:%M:%S")
	datas = sql.get_query(u"大气六参数", data, None, u"紧缩型时间传感器_实时时间")
	datas.reverse()
	sql.close_connect()
	datas_list_12 = []
	for data in datas:
		tmp = {}
		try:
			tmp["so2"] = float(data["SO2_SO2"]) * transform_factor["so2"]
		except:
			tmp["so2"] = data["SO2_SO2"]
		try:
			tmp["no2"] = float(data["NO2_NO2"]) * transform_factor["no2"]
		except:
			tmp["no2"] = data["NO2_NO2"]
		try:
			tmp["pm10"] = data["PM10_PM10"]
		except:
			tmp["pm10"] = data["PM10_PM10"]
		try:
			tmp["co"] = float(data["CO_CO"]) * transform_factor["co"]
		except:
			tmp["co"] = data["CO_CO"]
		try:
			tmp["o3"] = float(data["O3_O3"]) * transform_factor["o3"]
		except:
			tmp["o3"] = data["O3_O3"]
		tmp["pm25"] = data["PM2_5_PM2_5"]
		tmp["device_id"] = data[u"项目内节点编号"]
		tmp["time"] = str(data[u"紧缩型时间传感器_实时时间"])
		datas_list_12.append(tmp)
	for device in device_list:
		for data in datas_list_12:
			if device["id"] == data["device_id"]:
				device["latest_time"] = data["time"]
				break
	for data in datas_list_12:
		for device in device_list:
			if data["device_id"] == device["id"]:
				data["name"] = device["name"]
				data["time"] = str(data["time"])
				break
	# 统计监测点数量
	# device_list = [
	# 	{"id": 1, "name": u"京师方圆", "address": u"凤凰大道", "longitude": 117.2944, "latitude": 30.4127,
	# 	 "latest_time": "2016-11-22 12:00:00", "install_time": "2016-11-12 12:00:00"},
	# 	{"id": 2, "name": u"清风大道路", "address": u"新城区", "longitude": 117.2944, "latitude": 30.4027,
	# 	 "latest_time": "2016-11-22 12:00:00", "install_time": "2016-11-10 12:00:00"},
	# ]
	# device_list = devices
	device_len = len(device_list)

	# 正常工作点数量
	device_normal_len = device_len


	# 计算最近24小时站点均值
	# 首先获取最近24小时内所有站点的的数据
	# datas_list_12 = [
	# 	{"name": u"京师方圆", "so2": 32, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 158,
	# 	 "time": "2016-11-23 12:00:00"},
	# 	{"name": u"京师方圆", "so2": 32, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 158,
	# 	 "time": "2016-11-23 12:10:00"},
	# 	{"name": u"京师方圆", "so2": 32, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 158,
	# 	 "time": "2016-11-23 12:20:00"},
	# 	{"name": u"京师方圆", "so2": 32, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 158,
	# 	 "time": "2016-11-23 12:30:00"},
	# 	{"name": u"京师方圆", "so2": 32, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 158,
	# 	 "time": "2016-11-23 12:40:00"},
	# 	{"name": u"京师方圆", "so2": 32, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 158,
	# 	 "time": "2016-11-23 11:00:00"},
	# 	{"name": u"京师方圆", "so2": 32, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 158,
	# 	 "time": "2016-11-23 11:57:00"},
	# 	{"name": u"京师方圆", "so2": 32, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 158,
	# 	 "time": "2016-11-23 11:13:00"},
	# 	{"name": u"京师方圆", "so2": 32, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 158,
	# 	 "time": "2016-11-23 11:35:00"},
	# 	{"name": u"京师方圆", "so2": 32, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 158,
	# 	 "time": "2016-11-23 10:57:00"},
	# 	{"name": u"京师方圆", "so2": 32, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 158,
	# 	 "time": "2016-11-23 10:13:00"},
	# 	{"name": u"京师方圆", "so2": 32, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 158,
	# 	 "time": "2016-11-23 10:35:00"},
	# 	{"name": u"清风大道路", "so2": 32, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 158,
	# 	 "time": "2016-11-23 12:00:00"},
	# 	{"name": u"清风大道路", "so2": 32, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 158,
	# 	 "time": "2016-11-23 12:10:00"},
	# 	{"name": u"清风大道路", "so2": 32, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 158,
	# 	 "time": "2016-11-23 12:20:00"},
	# 	{"name": u"清风大道路", "so2": 32, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 158,
	# 	 "time": "2016-11-23 12:30:00"},
	# 	{"name": u"清风大道路", "so2": 32, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 158,
	# 	 "time": "2016-11-23 12:40:00"},
	# 	{"name": u"清风大道路", "so2": 32, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 158,
	# 	 "time": "2016-11-23 11:00:00"},
	# 	{"name": u"清风大道路", "so2": 32, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 158,
	# 	 "time": "2016-11-23 11:57:00"},
	# 	{"name": u"清风大道路", "so2": 32, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 158,
	# 	 "time": "2016-11-23 11:13:00"},
	# 	{"name": u"清风大道路", "so2": 32, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 158,
	# 	 "time": "2016-11-23 11:35:00"},
	# 	{"name": u"清风大道路", "so2": 32, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 158,
	# 	 "time": "2016-11-23 10:57:00"},
	# 	{"name": u"清风大道路", "so2": 32, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 158,
	# 	 "time": "2016-11-23 10:13:00"},
	# 	{"name": u"清风大道路", "so2": 32, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 158,
	# 	 "time": "2016-11-23 10:35:00"},
	# ]
	# datas_list_12 = datas
	# 计算各个数据的采集数量
	today = datetime.today()
	today_start = datetime(today.year,today.month,today.day,0,0,0)
	today_end = today_start + timedelta(days=1)
	today_data_no = 0
	for data in datas_list_12:
		time = datetime.strptime(data["time"], "%Y-%m-%d %H:%M:%S")
		if today_start <= time < today_end:
			today_data_no += 1
	pm25_len = today_data_no
	co_len = today_data_no
	no2_len = today_data_no
	so2_len = today_data_no
	pm10_len = today_data_no
	o3_len = today_data_no




	average_12 = []
	import time
	time_now = time.localtime(time.time())
	time_now_hour = time.localtime(time.time()).tm_hour
	print time_now
	twelve_data = {}
	twelve_data_hour = []
	twelve_data_data = {"so2": [], "no2": [], "pm10": [], "co": [], "o3": [], "pm25": []}
	factors = ["so2", "no2", "pm10", "co", "o3", "pm25"]
	for i in range(1, time_now_hour + 1):
		twelve_data_hour.append(str(i) + ":00")
		time_start = datetime(time_now.tm_year, time_now.tm_mon, time_now.tm_mday, i, 0, 0)
		time_end = datetime(time_now.tm_year, time_now.tm_mon, time_now.tm_mday, i, 0, 0) + timedelta(hours=1)
		print "start", time_start
		print "end", time_end
		for factor in factors:
			factor_sum = 0
			factor_num = 0
			for data in datas_list_12:
				time = datetime.strptime(data["time"], "%Y-%m-%d %H:%M:%S")
				print time
				if time_start <= time < time_end:
					try:
						factor_sum += data[factor]
						factor_num += 1
					except:
						pass
			try:
				twelve_data_data[factor].append(factor_sum / factor_num)
			except:
				twelve_data_data[factor].append(0)
	print twelve_data_hour
	print twelve_data_data
	twelve_data["twelve_data_hour"] = twelve_data_hour
	twelve_data["twelve_data_data"] = twelve_data_data
	return render(request, "admin/admin_index.html", {
		"twelve_data": twelve_data,
		"adminer": adminer,
		"pm25_len": pm25_len,
		"co_len": co_len,
		"no2_len": no2_len,
		"so2_len": so2_len,
		"pm10_len": pm10_len,
		"o3_len": o3_len,
		"device_len": device_len,
		"device_normal_len": device_normal_len,
	})
	# form = ItemUEditorModelForm(instance=item)