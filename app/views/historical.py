# coding=utf-8
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from dss.Serializer import serializer
import json
from objects.AqiParameter import AqiParameter
from datetime import datetime, timedelta


def historical_device(request):
	device_list = [
		{"id": 1, "name": u"京师方圆", "address" : u"凤凰大道", "longitude": 117.2944, "latitude": 30.4127, "latest_time":"2016-11-22 12:00:00", "install_time": "2016-11-12 12:00:00"},
		{"id": 2, "name": u"清风大道路", "address" : u"新城区", "longitude": 117.2944, "latitude": 30.4027, "latest_time":"2016-11-22 12:00:00", "install_time": "2016-11-10 12:00:00"},
	]
	device_data = [
		{"name": u"京师方圆", "so2": 32, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 158,"time": "2016-11-12 12:00:00"},
		{"name": u"清风大道路", "so2": 33, "no2": 20, "pm10": 20, "co": 2, "o3": 12, "pm25": 12,"time": "2016-11-12 12:00:00"}
	]
	for device in device_list:
		for data in device_data:
			if data["name"] == device["name"]:
				aqi = AqiParameter()
				aqi.get_1_aqi(data)
				device["AQI"] = aqi.AQI_1
				device["pm25"] = data["pm25"]
				device["so2"] = data["so2"]
				device["pm10"] = data["pm10"]
				break

	return render(request, "app/historical_device_list.html", {
		"device_list": device_list,
		"device_list_data": json.dumps(device_list),
	})


def historical_data(request):
	datas_list_all = [
		{"name": u"京师方圆", "so2": 32, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 158,
		 "time": "2016-11-22 12:00:00"},
		{"name": u"京师方圆", "so2": 12, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 158,
		 "time": "2016-11-22 12:10:00"},
		{"name": u"京师方圆", "so2": 22, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 158,
		 "time": "2016-11-22 12:20:00"},
		{"name": u"京师方圆", "so2": 32, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 158,
		 "time": "2016-11-22 12:30:00"},
		{"name": u"京师方圆", "so2": 42, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 158,
		 "time": "2016-11-22 12:40:00"},
		{"name": u"京师方圆", "so2": 52, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 158,
		 "time": "2016-11-22 11:00:00"},
		{"name": u"京师方圆", "so2": 62, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 158,
		 "time": "2016-11-22 11:57:00"},
		{"name": u"京师方圆", "so2": 72, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 158,
		 "time": "2016-11-22 11:13:00"},
		{"name": u"京师方圆", "so2": 82, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 158,
		 "time": "2016-11-22 11:35:00"},
		{"name": u"京师方圆", "so2": 92, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 158,
		 "time": "2016-11-22 10:57:00"},
		{"name": u"京师方圆", "so2": 102, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 158,
		 "time": "2016-11-22 10:13:00"},
		{"name": u"京师方圆", "so2": 112, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 158,
		 "time": "2016-11-22 10:35:00"},
		{"name": u"京师方圆", "so2": 122, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 158,
		 "time": "2016-11-22 09:00:00"},
		{"name": u"京师方圆", "so2": 132, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 158,
		 "time": "2016-11-22 08:10:00"},
		{"name": u"京师方圆", "so2": 142, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 158,
		 "time": "2016-11-22 07:20:00"},
		{"name": u"京师方圆", "so2": 152, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 158,
		 "time": "2016-11-22 06:30:00"},
		{"name": u"京师方圆", "so2": 162, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 158,
		 "time": "2016-11-22 05:40:00"},
		{"name": u"京师方圆", "so2": 172, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 158,
		 "time": "2016-11-22 04:00:00"},
		{"name": u"京师方圆", "so2": 182, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 158,
		 "time": "2016-11-22 03:57:00"},
		{"name": u"京师方圆", "so2": 192, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 158,
		 "time": "2016-11-22 02:13:00"},
		{"name": u"京师方圆", "so2": 202, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 158,
		 "time": "2016-11-22 01:35:00"},
		{"name": u"京师方圆", "so2": 22, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 158,
		 "time": "2016-11-22 00:57:00"},
		{"name": u"京师方圆", "so2": 32, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 158,
		 "time": "2016-11-21 23:13:00"},
		{"name": u"京师方圆", "so2": 42, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 158,
		 "time": "2016-11-21 22:35:00"},
	]
	# 计算今日数据
	import time
	time_now = time.localtime(time.time())
	time_now_hour = time.localtime(time.time()).tm_hour
	print time_now
	today_data = {}
	today_data_hour = []
	today_data_data = {"so2": [], "no2": [], "pm10": [], "co": [], "o3": [], "pm25": []}
	factors = ["so2", "no2", "pm10", "co", "o3", "pm25"]
	for i in range(1, time_now_hour + 1):
		today_data_hour.append(str(i) + ":00")
		time_start = datetime(time_now.tm_year, time_now.tm_mon, time_now.tm_mday, i, 0, 0)
		time_end = datetime(time_now.tm_year, time_now.tm_mon, time_now.tm_mday, i, 0, 0) + timedelta(hours=1)
		for factor in factors:
			factor_sum = 0
			factor_num = 0
			for data in datas_list_all:
				time = datetime.strptime(data["time"], "%Y-%m-%d %H:%M:%S")
				if time_start <= time < time_end:
					factor_sum += data[factor]
					factor_num += 1
			try:
				today_data_data[factor].append(factor_sum / factor_num)
			except:
				today_data_data[factor].append(0)
	today_data["today_data_hour"] = today_data_hour
	today_data["today_data_data"] = today_data_data
	# 计算一周日平均数据
	week_data = {}
	week_data_day = []
	week_data_data = {"so2": [], "no2": [], "pm10": [], "co": [], "o3": [], "pm25": []}
	factors = ["so2", "no2", "pm10", "co", "o3", "pm25"]
	for i in range(7):
		time_start = datetime(time_now.tm_year, time_now.tm_mon, time_now.tm_mday, 0, 0, 0) - timedelta(days=1)
		week_data_day.append(str(time_start.month) + u"月" + str(time_start.day) + u"号")
		time_end = time_start + timedelta(days=1)
		for factor in factors:
			factor_sum = 0
			factor_num = 0
			for data in datas_list_all:
				time = datetime.strptime(data["time"], "%Y-%m-%d %H:%M:%S")
				if time_start <= time < time_end:
					factor_sum += data[factor]
					factor_num += 1
			try:
				week_data_data[factor].append(factor_sum / factor_num)
			except:
				week_data_data[factor].append(0)
	week_data["week_data_day"] = week_data_day
	week_data["week_data_data"] = week_data_data
	# 计算当月日平均
	import time
	time_now_day = time.localtime(time.time()).tm_mday
	month_data = {}
	month_data_day = []
	month_data_data = {"so2": [], "no2": [], "pm10": [], "co": [], "o3": [], "pm25": []}
	factors = ["so2", "no2", "pm10", "co", "o3", "pm25"]
	for i in range(1,time_now_day+1):
		time_start = datetime(time_now.tm_year, time_now.tm_mon, 1, 0, 0, 0)
		month_data_day.append(str(time_start.month) + u"月" + str(time_start.day) + u"号")
		time_end = time_start + timedelta(days=1)
		for factor in factors:
			factor_sum = 0
			factor_num = 0
			for data in datas_list_all:
				time = datetime.strptime(data["time"], "%Y-%m-%d %H:%M:%S")
				if time_start <= time < time_end:
					factor_sum += data[factor]
					factor_num += 1
			try:
				month_data_data[factor].append(factor_sum / factor_num)
			except:
				month_data_data[factor].append(0)
	month_data["month_data_day"] = month_data_day
	month_data["month_data_data"] = month_data_data
	# 计算当年月平均
	import time
	time_now_month = time.localtime(time.time()).tm_mon
	year_data = {}
	year_data_month = []
	year_data_data = {"so2": [], "no2": [], "pm10": [], "co": [], "o3": [], "pm25": []}
	factors = ["so2", "no2", "pm10", "co", "o3", "pm25"]
	for i in range(1, time_now_month + 1):
		time_start = datetime(time_now.tm_year, 1, 1, 0, 0, 0)
		year_data_month.append(str(time_start.month) + u"月")
		import calendar
		monthRange = calendar.monthrange(time_now.tm_year, 1)
		time_end = time_start + timedelta(days=monthRange[1])
		for factor in factors:
			factor_sum = 0
			factor_num = 0
			for data in datas_list_all:
				time = datetime.strptime(data["time"], "%Y-%m-%d %H:%M:%S")
				if time_start <= time < time_end:
					factor_sum += data[factor]
					factor_num += 1
			try:
				year_data_data[factor].append(factor_sum / factor_num)
			except:
				year_data_data[factor].append(0)
	year_data["year_data_month"] = year_data_month
	year_data["year_data_data"] = year_data_data

	data = []
	data.append(today_data)
	data.append(week_data)
	data.append(month_data)
	data.append(year_data)
	# return HttpResponse(data)
	return render(request, "app/historical_data.html", {
		"data": json.dumps(data),
	})