# coding=utf-8
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from dss.Serializer import serializer
import json
from objects.AqiParameter import AqiParameter
from datetime import datetime, timedelta
from utils.mySqlUtils import MySQL


def index(request):
	sql = MySQL()
	sql.connectDB()
	datas = sql.get_query("data")
	devices = sql.get_query("device")
	sql.close_connect()
	datas_list = []
	for device in devices:
		for data in datas:
			if device["id"] == data["device_id"]:
				tmp = {}
				tmp["so2"] = data["so2"]
				tmp["no2"] = data["no2"]
				tmp["pm10"] = data["pm10"]
				tmp["co"] = data["co"]
				tmp["o3"] = data["o3"]
				tmp["pm25"] = data["pm25"]
				tmp["time"] = data["time"]
				tmp["name"] = device["name"]
				datas_list.append(tmp)
				break
	for data in datas:
		data["time"] = str(data["time"])
		for device in devices:
			if data["device_id"] == device["id"]:
				data["name"] = device["name"]
				break

	# 获取所有观测点的数据
	# datas_list = [
	# 	{"name": u"京师方圆","so2": 32, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 158, "time": "2016-11-12 12:00:00"},
	# 	{"name": u"清风大道路","so2": 33, "no2": 20, "pm10": 20, "co": 2, "o3": 12, "pm25": 12, "time": "2016-11-12 12:00:00"}
	# ]
	# data = [
	# 	{
	# 		"name":u"京师方圆", "main_pollute": u"细颗粒物(PM2.5)", "so2": 32, "no2": 53, "pm10": 294, "co": 2, "o3": 33,
	# 		"pm25": 158, "AQI": 188,"level": "五级", "classification": u"重度污染",
	# 		"health": u"心脏病和肺病患者症状显著加剧，运动耐受力降低，健康人群普遍出现症状",
	# 		"step": u"儿童，老年人及心脏病，呼吸系统疾病患者应停留在室内，停止户外运动，一般人群减少户外运动"
	# 	},
	# 	{
	# 		"name": u"清风大道路", "main_pollute": u"细颗粒物(PM2.5)", "so2": 33, "no2": 20, "pm10": 20, "co": 2, "o3": 12,
	# 		"pm25": 12, "AQI": 51, "level": "二级", "classification": u"良",
	# 		"health": u"空气质量可接受，但某些污染物可能对极少数异常敏感人群健康有较弱影响",
	# 		"step": u"极少数异常敏感人群应减少户外活动"
	# 	}
	# ]
	# 对所有的观测点进行数据平均计算AQI／PM2.5／首要污染物用于各监测点实时数据
	data_real_time = []
	for data in datas_list:
		calculator = AqiParameter()
		calculator.get_1_aqi(data)
		data["AQI_1"] = calculator.AQI_1
		data["Main_Pollute_1"] = calculator.Main_Pollute_1
		data["AQI_info_1"] = calculator.AQI_info_1
		data_real_time.append(data)
		print calculator
	# 计算各个站点实时采集数据的均值在首页的三个环圈显示
	average_data = {"so2": 0, "no2": 0, "pm10": 0, "co": 0, "o3": 0, "pm25": 0}
	for data in datas_list:
		average_data["so2"] += data["so2"]
		average_data["no2"] += data["no2"]
		average_data["pm10"] += data["pm10"]
		average_data["co"] += data["co"]
		average_data["o3"] += data["o3"]
		average_data["pm25"] += data["pm25"]
	average_data["so2"] /= len(datas_list)
	average_data["no2"] /= len(datas_list)
	average_data["pm10"] /= len(datas_list)
	average_data["co"] /= len(datas_list)
	average_data["o3"] /= len(datas_list)
	average_data["pm25"] /= len(datas_list)
	calculator = AqiParameter()
	calculator.get_1_aqi(average_data)
	average_data["AQI_1"] = calculator.AQI_1
	average_data["Main_Pollute_1"] = calculator.Main_Pollute_1
	average_data["AQI_info_1"] = calculator.AQI_info_1
	# 计算最近24小时站点均值
	# 首先获取最近24小时内所有站点的的数据
	datas_list_12 = [
		{"name": u"京师方圆", "so2": 32, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 158, "time": "2016-11-23 12:00:00"},
		{"name": u"京师方圆", "so2": 32, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 158, "time": "2016-11-23 12:10:00"},
		{"name": u"京师方圆", "so2": 32, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 158, "time": "2016-11-23 12:20:00"},
		{"name": u"京师方圆", "so2": 32, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 158, "time": "2016-11-23 12:30:00"},
		{"name": u"京师方圆", "so2": 32, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 158, "time": "2016-11-23 12:40:00"},
		{"name": u"京师方圆", "so2": 32, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 158, "time": "2016-11-23 11:00:00"},
		{"name": u"京师方圆", "so2": 32, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 158, "time": "2016-11-23 11:57:00"},
		{"name": u"京师方圆", "so2": 32, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 158, "time": "2016-11-23 11:13:00"},
		{"name": u"京师方圆", "so2": 32, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 158, "time": "2016-11-23 11:35:00"},
		{"name": u"京师方圆", "so2": 32, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 158, "time": "2016-11-23 10:57:00"},
		{"name": u"京师方圆", "so2": 32, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 158, "time": "2016-11-23 10:13:00"},
		{"name": u"京师方圆", "so2": 32, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 158, "time": "2016-11-23 10:35:00"},
		{"name": u"清风大道路", "so2": 32, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 158, "time": "2016-11-23 12:00:00"},
		{"name": u"清风大道路", "so2": 32, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 158, "time": "2016-11-23 12:10:00"},
		{"name": u"清风大道路", "so2": 32, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 158, "time": "2016-11-23 12:20:00"},
		{"name": u"清风大道路", "so2": 32, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 158, "time": "2016-11-23 12:30:00"},
		{"name": u"清风大道路", "so2": 32, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 158, "time": "2016-11-23 12:40:00"},
		{"name": u"清风大道路", "so2": 32, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 158, "time": "2016-11-23 11:00:00"},
		{"name": u"清风大道路", "so2": 32, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 158, "time": "2016-11-23 11:57:00"},
		{"name": u"清风大道路", "so2": 32, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 158, "time": "2016-11-23 11:13:00"},
		{"name": u"清风大道路", "so2": 32, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 158, "time": "2016-11-23 11:35:00"},
		{"name": u"清风大道路", "so2": 32, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 158, "time": "2016-11-23 10:57:00"},
		{"name": u"清风大道路", "so2": 32, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 158, "time": "2016-11-23 10:13:00"},
		{"name": u"清风大道路", "so2": 32, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 158, "time": "2016-11-23 10:35:00"},
	]
	datas_list_12 = datas
	average_12 = []
	import time
	time_now = time.localtime(time.time())
	time_now_hour = time.localtime(time.time()).tm_hour
	print time_now
	twelve_data = {}
	twelve_data_hour = []
	twelve_data_data = {"so2":[], "no2":[], "pm10":[], "co":[], "o3":[], "pm25":[]}
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
					factor_sum += data[factor]
					factor_num += 1
			try:
				twelve_data_data[factor].append(factor_sum/factor_num)
			except:
				twelve_data_data[factor].append(0)
	print twelve_data_hour
	print twelve_data_data
	twelve_data["twelve_data_hour"] = twelve_data_hour
	twelve_data["twelve_data_data"] = twelve_data_data
	return render(request, "app/index.html", {
		"twelve_data": twelve_data,
		"average_data": average_data,
		"data_real_time": data_real_time,
	})