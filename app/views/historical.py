# coding=utf-8
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from dss.Serializer import serializer
import json
from objects.AqiParameter import AqiParameter
from datetime import datetime, timedelta
from app.models import Adminer
from objects.AqiParameter import AqiParameter
from utils.mySqlUtils import MySQL
import math
transform_factor = {"so2": 2949.276785714286, "o3": 2142.7767857142856, "co": 1.2504464285714287, "no2": 2054.017857142857}
import random
def historical_device(request):
	try:
		adminer = Adminer.objects.get(username=request.session["username"])
	except:
		return HttpResponseRedirect("/user_login/")
	sql = MySQL()
	sql.connectDB("projectmanagement")
	data = {}
	data["ProjectID"] = {}
	data["ProjectID"]["conn"] = "="
	data["ProjectID"]["val"] = str(1)
	devices = sql.get_query("projectnodeinfo", data)
	sql.close_connect()
	device_list = []
	admin_ndoe_list = adminer.admin_node.split(',')
	print "admin_node_list"
	print admin_ndoe_list
	for device in devices:
		tmp = {}
		tmp["id"] = device["NodeNO"]
		tmp["name"] = device["Description"]
		tmp["address"] = device["InstallationAddress"]
		if int(tmp["id"]) == 1:
			tmp["longitude"] = str(117.5379210000)
			tmp["latitude"] = str(30.6916740000)
		elif int(tmp["id"]) == 2:
			tmp["longitude"] = str(117.5433630000)
			tmp["latitude"] = str(30.7021370000)
		elif int(tmp["id"]) == 3:
			tmp["longitude"] = str(117.5442090000)
			tmp["latitude"] = str(30.7166530000)
		elif int(tmp["id"]) == 4:
			tmp["longitude"] = str(117.5497670000)
			tmp["latitude"] = str(30.7098570000)
		elif int(tmp["id"]) == 5:
			tmp["longitude"] = str(117.5619360000)
			tmp["latitude"] = str(30.7385770000)
		elif int(tmp["id"]) == 6:
			tmp["longitude"] = str(118.3440090000)
			tmp["latitude"] = str(30.9235910000)
		else:
			tmp["longitude"] = str(117.5436320000 + 0.01 * random.randint(-2, 2))
			tmp["latitude"] = str(30.7078830000 + 0.01 * random.randint(-3, 3))
		tmp["install_time"] = str(device["SetTime"])
		if unicode(tmp["id"]) in admin_ndoe_list:
			device_list.append(tmp)
	devices = device_list
	sql.connectDB("jssf")
	datas = sql.get_query(u"大气六参数", None, None, u"紧缩型时间传感器_实时时间")
	datas.reverse()
	sql.close_connect()
	datas_list_briage = []
	for data in datas:
		tmp = {}
		try:
			tmp["so2"] = round(float(data["SO2_SO2"]) * transform_factor["so2"],3)
		except:
			tmp["so2"] = data["SO2_SO2"]
		try:
			tmp["no2"] = round(float(data["NO2_NO2"]) * transform_factor["no2"],3)
		except:
			tmp["no2"] = data["NO2_NO2"]
		try:
			tmp["pm10"] = data["PM10_PM10"]
		except:
			tmp["pm10"] = data["PM10_PM10"]
		try:
			tmp["co"] = round(float(data["CO_CO"]) * transform_factor["co"],3)
		except:
			tmp["co"] = data["CO_CO"]
		try:
			tmp["o3"] = round(float(data["O3_O3"]) * transform_factor["o3"],3)
		except:
			tmp["o3"] = data["O3_O3"]
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


def historical_data_list(request,device_id):
	try:
		adminer = Adminer.objects.get(username=request.session["username"])
	except:
		return HttpResponseRedirect("/user_login/")
	try:
		sql = MySQL()
		sql.connectDB("projectmanagement")
		data = {}
		data["NodeNo"] = {}
		data["NodeNo"]["conn"] = "="
		data["NodeNo"]["val"] = str(device_id)
		device = sql.get_query("projectnodeinfo", data)[0]
		sql.close_connect()
	except Exception as e:
		print str(e)
		return HttpResponse("没有数据")
	device["id"] = device["NodeNO"]
	device["name"] = device["Description"]
	device["address"] = device["InstallationAddress"]
	device["longitude"] = "117.5436320000"
	device["latitude"] = "30.7078830000"
	device["install_time"] = str(device["SetTime"])
	try:
		page = int(request.GET.get("page"))
	except:
		page = 1
	# 页码
	if page < 1:
		return HttpResponseRedirect("/historical_device_data_list/1")
	# 时间
	try:
		start_time = request.GET.get("data_time", None)
		today = datetime.today()
		if start_time is None:
			start_time = datetime(today.year, today.month, today.day, 0, 0, 0)
			start_time = str(start_time)[0:10]
			return HttpResponseRedirect("/historical_device_data_list/" + str(device["id"]) + "?data_time=" + start_time)
			end_time = start_time + timedelta(days=1)
		else:
			start_time += " 00:00:00"
			start_time = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
			end_time = start_time + timedelta(days=1)
		sql = MySQL()
		sql.connectDB("jssf")
		datas = sql.get_query_s_e_time(u"大气六参数", str(device["id"]), u"紧缩型时间传感器_实时时间", str(start_time), str(end_time), None, u"紧缩型时间传感器_实时时间")
		sql.close_connect()
		datas_list_briage = []
		for data in datas:
			tmp = {}
			try:
				tmp["so2"] = round(float(data["SO2_SO2"]) * transform_factor["so2"],3)
			except:
				tmp["so2"] = data["SO2_SO2"]
			try:
				tmp["no2"] = round(float(data["NO2_NO2"]) * transform_factor["no2"],3)
			except:
				tmp["no2"] = data["NO2_NO2"]
			try:
				tmp["pm10"] = data["PM10_PM10"]
			except:
				tmp["pm10"] = data["PM10_PM10"]
			try:
				tmp["co"] = round(float(data["CO_CO"]) * transform_factor["co"],3)
			except:
				tmp["co"] = data["CO_CO"]
			try:
				tmp["o3"] = round(float(data["O3_O3"]) * transform_factor["o3"],3)
			except:
				tmp["o3"] = data["O3_O3"]
			tmp["pm25"] = data["PM2_5_PM2_5"]
			tmp["device_id"] = data[u"项目内节点编号"]
			tmp["time"] = str(data[u"紧缩型时间传感器_实时时间"])
			datas_list_briage.append(tmp)
		datas = datas_list_briage
		for data in datas:
			data["name"] = device["name"]
			data["time"] = str(data["time"])
			calculator = AqiParameter()
			calculator.get_1_aqi(data)
			data["AQI_1"] = calculator.AQI_1
			data["Main_Pollute_1"] = calculator.Main_Pollute_1
			data["AQI_info_1"] = calculator.AQI_info_1
	except Exception as e:
		print str(e)
		datas = []
		pass
	total_page = int(math.ceil(len(datas)/20.0))
	if total_page < 1:
		total_page = 1
	if page > total_page:
		return HttpResponseRedirect("/historical_device_data_list/" + device["id"] + str(total_page))
	today_data = {}
	today_data_time = []
	today_data_data = {"so2": [], "no2": [], "pm10": [], "co": [], "o3": [], "pm25": []}
	factors = ["so2", "no2", "pm10", "co", "o3", "pm25"]
	for data in datas:
		today_data_time.append(data["time"])
		for factor in factors:
			try:
				today_data_data[factor].append(float(data[factor]))
			except:
				pass
	today_data["today_data_time"] = today_data_time
	today_data["today_data_data"] = today_data_data

	# 获取当前数据的每20条
	start_num = (page - 1) * 20
	end_num = page * 20
	datas = datas[start_num:end_num]
	# 参数
	try:
		parameter = request.GET.get("parameter", "pm25")
	except:
		parameter = "pm25"

	return render(request, "app/historical_data_list.html", {
		"page": page,
		"total_page": total_page,
		"data_time": start_time,
		"data_list": datas,
		"parameter": parameter,
		"device": device,
		"today_data": today_data,
	})


def historical_data_analysis(request,device_id):
	try:
		adminer = Adminer.objects.get(username=request.session["username"])
	except:
		return HttpResponseRedirect("/user_login/")
	try:
		device = {"id": 1, "name": "京师方圆"}
		sql = MySQL()
		sql.connectDB("projectmanagement")
		data = {}
		data["NodeNo"] = {}
		data["NodeNo"]["conn"] = "="
		data["NodeNo"]["val"] = str(device_id)
		device = sql.get_query("projectnodeinfo", data)[0]
		sql.close_connect()
		# print device
	except Exception as e:
		print str(e)
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
	data = {}
	data[u"项目内节点编号"] = {}
	data[u"项目内节点编号"]["conn"] = "="
	data[u"项目内节点编号"]["val"] = str(device["id"])
	datas = sql.get_query(u"大气六参数",data, None, u"紧缩型时间传感器_实时时间")
	datas.reverse()
	sql.close_connect()
	datas_list_briage = []
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
				elif time < time_start:
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
				elif time < time_start:
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
				elif time < time_start:
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
				elif time < time_start:
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


def historical_voltage_list(request):
	try:
		adminer = Adminer.objects.get(username=request.session["username"])
	except:
		return HttpResponseRedirect("/user_login/")
	try:
		adminer_node = adminer.admin_node.split(',')
		device_id = request.GET.get("device_id")
		if unicode(device_id) not in adminer_node:
			device_id = int(adminer_node[0])
	except Exception as e:
		print(str(e))
		adminer_node = int(adminer.admin_node.split(',')[0])
		device_id = adminer_node
	sql = MySQL()
	# 获取设备列表
	sql.connectDB("projectmanagement")
	data = {}
	data["ProjectID"] = {}
	data["ProjectID"]["conn"] = "="
	data["ProjectID"]["val"] = str(1)
	device_list = sql.get_query("projectnodeinfo", data, None)
	sql.close_connect()
	print device_list
	device_list_briage = []
	admin_ndoe_list = adminer.admin_node.split(',')
	for device_t in device_list:
		tmp = {}
		tmp["name"] = device_t["Description"]
		tmp["id"] = device_t["NodeNO"]
		tmp["address"] = device_t["InstallationAddress"]
		tmp["longitude"] = "117.5436320000"
		tmp["latitude"] = "30.7078830000"
		tmp["install_time"] = device_t["SetTime"]
		if unicode(tmp["id"]) in admin_ndoe_list:
			device_list_briage.append(tmp)
	device_list = device_list_briage

	try:
		sql = MySQL()
		sql.connectDB("projectmanagement")
		data = {}
		data["NodeNo"] = {}
		data["NodeNo"]["conn"] = "="
		data["NodeNo"]["val"] = str(device_id)
		device = sql.get_query("projectnodeinfo", data)[0]
		sql.close_connect()
	except Exception as e:
		print str(e)
		return HttpResponse("没有数据")
	device["id"] = device["NodeNO"]
	device["name"] = device["Description"]
	device["address"] = device["InstallationAddress"]
	device["longitude"] = "117.5436320000"
	device["latitude"] = "30.7078830000"
	device["install_time"] = str(device["SetTime"])
	try:
		page = int(request.GET.get("page"))
	except:
		page = 1
	# 页码
	if page < 1:
		return HttpResponseRedirect("/voltage/?device_id=1")
	# 时间
	try:
		start_time = request.GET.get("data_time", None)
		today = datetime.today()
		if start_time is None:
			start_time = datetime(today.year, today.month, today.day, 0, 0, 0)
			start_time = str(start_time)[0:10]
			return HttpResponseRedirect("/voltage/?device_id=" + str(device["id"]) + "?data_time=" + start_time)
			end_time = start_time + timedelta(days=1)
		else:
			start_time += " 00:00:00"
			start_time = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
			end_time = start_time + timedelta(days=1)
		sql = MySQL()
		sql.connectDB("jssf")
		datas = sql.get_query_s_e_time(u"大气六参数", str(device["id"]), u"紧缩型时间传感器_实时时间", str(start_time), str(end_time), None, u"紧缩型时间传感器_实时时间")
		sql.close_connect()
		datas_list_briage = []
		for data in datas:
			tmp = {}
			try:
				tmp["so2"] = round(float(data["SO2_SO2"]) * transform_factor["so2"],3)
			except:
				tmp["so2"] = data["SO2_SO2"]
			try:
				tmp["no2"] = round(float(data["NO2_NO2"]) * transform_factor["no2"],3)
			except:
				tmp["no2"] = data["NO2_NO2"]
			try:
				tmp["pm10"] = data["PM10_PM10"]
			except:
				tmp["pm10"] = data["PM10_PM10"]
			try:
				tmp["co"] = round(float(data["CO_CO"]) * transform_factor["co"],3)
			except:
				tmp["co"] = data["CO_CO"]
			try:
				tmp["o3"] = round(float(data["O3_O3"]) * transform_factor["o3"],3)
			except:
				tmp["o3"] = data["O3_O3"]
			tmp["pm25"] = data["PM2_5_PM2_5"]
			tmp["voltage"] = data[u"电池电压传感器_电压"]
			tmp["device_id"] = data[u"项目内节点编号"]
			tmp["time"] = str(data[u"紧缩型时间传感器_实时时间"])
			datas_list_briage.append(tmp)
		datas = datas_list_briage
		for data in datas:
			data["name"] = device["name"]
			data["time"] = str(data["time"])
			calculator = AqiParameter()
			calculator.get_1_aqi(data)
			data["AQI_1"] = calculator.AQI_1
			data["Main_Pollute_1"] = calculator.Main_Pollute_1
			data["AQI_info_1"] = calculator.AQI_info_1
	except Exception as e:
		print str(e)
		datas = []
		pass
	total_page = int(math.ceil(len(datas)/20.0))
	if total_page < 1:
		total_page = 1
	if page > total_page:
		return HttpResponseRedirect("/voltage/?device_id=" + device["id"] + "&total_page=" + str(total_page))
	today_data = {}
	today_data_time = []
	today_data_data = {"so2": [], "no2": [], "pm10": [], "co": [], "o3": [], "pm25": [], "voltage": []}
	factors = ["so2", "no2", "pm10", "co", "o3", "pm25", "voltage"]
	for data in datas:
		today_data_time.append(data["time"])
		for factor in factors:
			try:
				today_data_data[factor].append(float(data[factor]))
			except:
				pass
	today_data["today_data_time"] = today_data_time
	today_data["today_data_data"] = today_data_data

	# 获取当前数据的每20条
	start_num = (page - 1) * 20
	end_num = page * 20
	datas = datas[start_num:end_num]
	# 参数
	try:
		parameter = request.GET.get("parameter", "pm25")
	except:
		parameter = "pm25"

	return render(request, "app/historical_voltage_list.html", {
		"page": page,
		"total_page": total_page,
		"data_time": start_time,
		"data_list": datas,
		"parameter": parameter,
		"device": device,
		"today_data": today_data,
		"device_list": device_list,
	})