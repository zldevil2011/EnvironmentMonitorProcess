# coding=utf-8
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from dss.Serializer import serializer
import json
from objects.AqiParameter import AqiParameter
from datetime import datetime, timedelta
from objects.AqiParameter import AqiParameter
from utils.mySqlUtils import MySQL
transform_factor = {"so2": 2949.276785714286, "o3": 2142.7767857142856, "co": 1250.4464285714287, "no2": 2054.017857142857}

def historical_device(request):
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
		tmp["install_time"] = str(device["SetTime"])
		device_list.append(tmp)
	devices = device_list
	sql.connectDB("jssf")
	datas = sql.get_query(u"大气六参数", None, None, None, None, u"紧缩型时间传感器_实时时间")
	datas.reverse()
	sql.close_connect()
	datas_list_briage = []
	for data in datas:
		tmp = {}
		tmp["so2"] = data["SO2_SO2"] * transform_factor["so2"]
		tmp["no2"] = data["NO2_NO2"] * transform_factor["no2"]
		tmp["pm10"] = data["PM10_PM10"]
		tmp["co"] = data["CO_CO"] * transform_factor["co"]
		tmp["o3"] = data["O3_O3"] * transform_factor["o3"]
		tmp["pm25"] = data["PM2_5_PM2_5"]
		tmp["device_id"] = data[u"项目内节点编号"]
		tmp["time"] = str(data[u"紧缩型时间传感器_实时时间"])
		datas_list_briage.append(tmp)
	datas = datas_list_briage
	for device in devices:
		for data in datas:
			if device["id"] == data["device_id"]:
				device["latest_time"] = str(data["time"])
				break
	device_data = []
	for device in devices:
		for data in datas:
			if data["device_id"] == device["id"]:
				tmp = {}
				tmp["name"] = device["name"]
				tmp["so2"] = data["so2"]
				tmp["no2"] = data["no2"]
				tmp["pm10"] = data["pm10"]
				tmp["co"] = data["co"]
				tmp["o3"] = data["o3"]
				tmp["pm25"] = data["pm25"]
				tmp["time"] = str(data["time"])
				device_data.append(tmp)
				break
	# 设备列表
	device_list = [
		{"id": 1, "name": u"京师方圆", "address" : u"凤凰大道", "longitude": 117.2944, "latitude": 30.4127, "latest_time":"2016-11-22 12:00:00", "install_time": "2016-11-12 12:00:00"},
		{"id": 2, "name": u"清风大道路", "address" : u"新城区", "longitude": 117.2944, "latitude": 30.4027, "latest_time":"2016-11-22 12:00:00", "install_time": "2016-11-10 12:00:00"},
	]
	device_list = devices
	# 每个站点最新的一条数据
	# device_data = [
	# 	{"name": u"京师方圆", "so2": 32, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 158,"time": "2016-11-12 12:00:00"},
	# 	{"name": u"清风大道路", "so2": 33, "no2": 20, "pm10": 20, "co": 2, "o3": 12, "pm25": 12,"time": "2016-11-12 12:00:00"}
	# ]
	for device in device_list:
		flag = 0
		for data in device_data:
			if data["name"] == device["name"]:
				aqi = AqiParameter()
				aqi.get_1_aqi(data)
				device["AQI"] = aqi.AQI_1
				device["pm25"] = data["pm25"]
				device["so2"] = data["so2"]
				device["pm10"] = data["pm10"]
				flag = 1
				break
		if flag == 0:
			device["AQI"] = u"无数据"
			device["pm25"] = u"无数据"
			device["so2"] = u"无数据"
			device["pm10"] = u"无数据"

	return render(request, "app/historical_device_list.html", {
		"device_list": device_list,
		"device_list_data": json.dumps(device_list),
	})


def get_aqi(data):
	cal = AqiParameter()
	cal.get_1_aqi(data)
	return cal.AQI_1


def historical_data(request,device_id):
	try:
		device = {"id": 1, "name": "京师方圆"}
		sql = MySQL()
		sql.connectDB("projectmanagement")
		device = sql.get_query("projectnodeinfo", "NodeNo", "=", str(device_id))[0]
		sql.close_connect()
		# print device
	except:
		try:
			sql = MySQL()
			sql.connectDB("projectmanagement")
			device = sql.get_query("projectnodeinfo", "ProjectID", "=", "1")[0]
			sql.close_connect()
		except:
			return HttpResponse("没有数据")
	device["id"] = device["NodeNO"]
	device["name"] = device["Description"]
	device["address"] = device["InstallationAddress"]
	device["longitude"] = "117.5436320000"
	device["latitude"] = "30.7078830000"
	device["install_time"] = str(device["SetTime"])
	sql.connectDB("jssf")
	datas = sql.get_query(u"大气六参数",u"项目内节点编号","=", str(device["id"]), None, u"紧缩型时间传感器_实时时间")
	datas.reverse()
	sql.close_connect()
	datas_list_briage = []
	for data in datas:
		tmp = {}
		tmp["so2"] = data["SO2_SO2"] * transform_factor["so2"]
		tmp["no2"] = data["NO2_NO2"] * transform_factor["no2"]
		tmp["pm10"] = data["PM10_PM10"]
		tmp["co"] = data["CO_CO"] * transform_factor["no"]
		tmp["o3"] = data["O3_O3"] * transform_factor["o3"]
		tmp["pm25"] = data["PM2_5_PM2_5"]
		tmp["device_id"] = data[u"项目内节点编号"]
		tmp["time"] = str(data[u"紧缩型时间传感器_实时时间"])
		datas_list_briage.append(tmp)
	datas = datas_list_briage
	for data in datas:
		data["name"] = device["name"]
		data["time"] = str(data["time"])
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
		{"name": u"京师方圆", "so2": 202, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 12,
		 "time": "2016-11-22 01:35:00"},
		{"name": u"京师方圆", "so2": 22, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 12,
		 "time": "2016-11-22 00:57:00"},
		{"name": u"京师方圆", "so2": 32, "no2": 53, "pm10": 10, "co": 2, "o3": 33, "pm25": 12,
		 "time": "2016-11-21 23:13:00"},
		{"name": u"京师方圆", "so2": 42, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 12,
		 "time": "2016-11-21 22:35:00"},
	]
	datas_list_all = datas
	# 计算今日数据
	import time
	time_now = time.localtime(time.time())
	time_now_hour = time.localtime(time.time()).tm_hour
	# print time_now
	today_data = {}
	today_data_hour = []
	today_data_min_aqi = {"today_data_min_aqi_date": "", "today_data_min_aqi_val": 0}
	today_data_max_aqi = {"today_data_max_aqi_date": "", "today_data_max_aqi_val": 0}
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
				aqi = get_aqi(data)
				time = datetime.strptime(data["time"], "%Y-%m-%d %H:%M:%S")
				if time_start <= time < time_end:
					try:
						factor_sum += data[factor]
					except:
						factor_sum += 0
					factor_num += 1
					if today_data_min_aqi["today_data_min_aqi_val"] == 0:
						today_data_min_aqi["today_data_min_aqi_val"] = aqi
						today_data_min_aqi["today_data_min_aqi_date"] = data["time"]
					elif aqi < today_data_min_aqi["today_data_min_aqi_val"]:
						today_data_min_aqi["today_data_min_aqi_val"] = aqi
						today_data_min_aqi["today_data_min_aqi_date"] = data["time"]
					if aqi > today_data_max_aqi["today_data_max_aqi_val"]:
						today_data_max_aqi["today_data_max_aqi_val"] = aqi
						today_data_max_aqi["today_data_max_aqi_date"] = data["time"]
				elif time >= time_end:
					break
			try:
				today_data_data[factor].append(factor_sum / factor_num)
			except:
				today_data_data[factor].append(0)
	today_data["today_data_hour"] = today_data_hour
	today_data["today_data_data"] = today_data_data
	today_data["today_data_min_aqi"] = today_data_min_aqi
	today_data["today_data_max_aqi"] = today_data_max_aqi
	# 计算一周日平均数据
	week_data = {}
	week_data_day = []
	week_data_min_aqi = {"week_data_min_aqi_date": "", "week_data_min_aqi_val": 0}
	week_data_max_aqi = {"week_data_max_aqi_date": "", "week_data_max_aqi_val": 0}
	week_data_data = {"so2": [], "no2": [], "pm10": [], "co": [], "o3": [], "pm25": []}
	factors = ["so2", "no2", "pm10", "co", "o3", "pm25"]
	for i in range(7):
		time_start = datetime(time_now.tm_year, time_now.tm_mon, time_now.tm_mday, 0, 0, 0) - timedelta(days=i)
		week_data_day.append(str(time_start.month) + u"月" + str(time_start.day) + u"号")
		time_end = time_start + timedelta(days=1)
		for factor in factors:
			factor_sum = 0
			factor_num = 0
			for data in datas_list_all:
				aqi = get_aqi(data)
				time = datetime.strptime(data["time"], "%Y-%m-%d %H:%M:%S")
				if time_start <= time < time_end:
					try:
						factor_sum += data[factor]
					except:
						factor_sum += 0
					factor_num += 1
					if week_data_min_aqi["week_data_min_aqi_val"] == 0:
						week_data_min_aqi["week_data_min_aqi_val"] = aqi
						week_data_min_aqi["week_data_min_aqi_date"] = data["time"]
					elif aqi < week_data_min_aqi["week_data_min_aqi_val"]:
						week_data_min_aqi["week_data_min_aqi_val"] = aqi
						week_data_min_aqi["week_data_min_aqi_date"] = data["time"]
					if aqi > week_data_max_aqi["week_data_max_aqi_val"]:
						week_data_max_aqi["week_data_max_aqi_val"] = aqi
						week_data_max_aqi["week_data_max_aqi_date"] = data["time"]
				elif time >= time_end:
					break
			try:
				week_data_data[factor].append(factor_sum / factor_num)
			except:
				week_data_data[factor].append(0)
	week_data_day.reverse()
	week_data["week_data_day"] = week_data_day
	for factor in factors:
		week_data_data[factor].reverse()
	week_data["week_data_data"] = week_data_data
	week_data["week_data_min_aqi"] = week_data_min_aqi
	week_data["week_data_max_aqi"] = week_data_max_aqi
	# 计算当月日平均
	import time
	time_now_day = time.localtime(time.time()).tm_mday
	month_data = {}
	month_data_day = []
	month_data_min_aqi = {"month_data_min_aqi_date": "", "month_data_min_aqi_val": 0}
	month_data_max_aqi = {"month_data_max_aqi_date": "", "month_data_max_aqi_val": 0}
	month_data_data = {"so2": [], "no2": [], "pm10": [], "co": [], "o3": [], "pm25": []}
	factors = ["so2", "no2", "pm10", "co", "o3", "pm25"]
	for i in range(1,time_now_day+1):
		time_start = datetime(time_now.tm_year, time_now.tm_mon, i, 0, 0, 0)
		month_data_day.append(str(time_start.day) + u"号")
		time_end = time_start + timedelta(days=1)
		for factor in factors:
			factor_sum = 0
			factor_num = 0
			for data in datas_list_all:
				aqi = get_aqi(data)
				time = datetime.strptime(data["time"], "%Y-%m-%d %H:%M:%S")
				if time_start <= time < time_end:
					try:
						factor_sum += data[factor]
					except:
						factor_sum += 0
					factor_num += 1
					if month_data_min_aqi["month_data_min_aqi_val"] == 0:
						month_data_min_aqi["month_data_min_aqi_val"] = aqi
						month_data_min_aqi["month_data_min_aqi_date"] = data["time"]
					elif aqi < month_data_min_aqi["month_data_min_aqi_val"]:
						month_data_min_aqi["month_data_min_aqi_val"] = aqi
						month_data_min_aqi["month_data_min_aqi_date"] = data["time"]
					if aqi > month_data_max_aqi["month_data_max_aqi_val"]:
						month_data_max_aqi["month_data_max_aqi_val"] = aqi
						month_data_max_aqi["month_data_max_aqi_date"] = data["time"]
				elif time >= time_end:
					break
			try:
				month_data_data[factor].append(factor_sum / factor_num)
			except:
				month_data_data[factor].append(0)
	month_data["month_data_day"] = month_data_day
	month_data["month_data_data"] = month_data_data
	month_data["month_data_min_aqi"] = month_data_min_aqi
	month_data["month_data_max_aqi"] = month_data_max_aqi
	# 计算当年月平均
	import time
	time_now_month = time.localtime(time.time()).tm_mon
	year_data = {}
	year_data_month = []
	year_data_min_aqi = {"year_data_min_aqi_date": "", "year_data_min_aqi_val": 0}
	year_data_max_aqi = {"year_data_max_aqi_date": "", "year_data_max_aqi_val": 0}
	year_data_data = {"so2": [], "no2": [], "pm10": [], "co": [], "o3": [], "pm25": []}
	factors = ["so2", "no2", "pm10", "co", "o3", "pm25"]
	for i in range(1, time_now_month + 1):
		time_start = datetime(time_now.tm_year, i, 1, 0, 0, 0)
		year_data_month.append(str(time_start.month) + u"月")
		import calendar
		monthRange = calendar.monthrange(time_now.tm_year, 1)
		time_end = time_start + timedelta(days=monthRange[1])
		for factor in factors:
			factor_sum = 0
			factor_num = 0
			for data in datas_list_all:
				aqi = get_aqi(data)
				time = datetime.strptime(data["time"], "%Y-%m-%d %H:%M:%S")
				if time_start <= time < time_end:
					try:
						factor_sum += data[factor]
					except:
						factor_sum += 0
					factor_num += 1
					if year_data_min_aqi["year_data_min_aqi_val"] == 0:
						year_data_min_aqi["year_data_min_aqi_val"] = aqi
						year_data_min_aqi["year_data_min_aqi_date"] = data["time"]
					elif aqi < year_data_min_aqi["year_data_min_aqi_val"]:
						year_data_min_aqi["year_data_min_aqi_val"] = aqi
						year_data_min_aqi["year_data_min_aqi_date"] = data["time"]
					if aqi > year_data_max_aqi["year_data_max_aqi_val"]:
						year_data_max_aqi["year_data_max_aqi_val"] = aqi
						year_data_max_aqi["year_data_max_aqi_date"] = data["time"]
				elif time >= time_end:
					break
			try:
				year_data_data[factor].append(factor_sum / factor_num)
			except:
				year_data_data[factor].append(0)
	year_data["year_data_month"] = year_data_month
	year_data["year_data_data"] = year_data_data
	year_data["year_data_min_aqi"] = year_data_min_aqi
	year_data["year_data_max_aqi"] = year_data_max_aqi
	data = {}
	data["today_data"] = today_data
	data["week_data"] = week_data
	data["month_data"] = month_data
	data["year_data"] = year_data
	# return HttpResponse(data)
	return render(request, "app/historical_data.html", {
		"data": json.dumps(data),
		"device": device,
	})