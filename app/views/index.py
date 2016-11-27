# coding=utf-8
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from dss.Serializer import serializer
import json
from objects.AqiParameter import AqiParameter
from datetime import datetime, timedelta
from utils.mySqlUtils import MySQL
from django.core.mail import send_mail
from EMP import settings


def index(request):
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
	NOW = datetime.today()
	start = datetime(NOW.year, NOW.month, NOW.day, 0, 0, 0)
	sql.connectDB("jssf")
	datas = sql.get_query(u"大气六参数", u"紧缩型时间传感器_实时时间", ">", start.strftime("%Y-%m-%d %H:%M:%S"), None, u"紧缩型时间传感器_实时时间")
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
		data_collect_time = data["time"]
		warning_time = datetime.today()
		warning_time = datetime(warning_time.year, warning_time.month, warning_time.day, warning_time.hour, 0, 0)
		if int(calculator.AQI_1) >= 150 and data_collect_time > warning_time:
			subject = u"污染指数通知"
			text_content = u"观测设备" + data["name"] + u"在" + str(data["time"]) + u"AQI值为" + str(calculator.AQI_1) + u",污染程度:" + unicode(calculator.AQI_info_1["classification"])
			from_email = settings.EMAIL_HOST_USER
			to = "929034478@qq.com"
			try:
				send_mail(subject, text_content, from_email, [to], fail_silently=False)
			except Exception as e:
				pass
	# 计算各个站点实时采集数据的均值在首页的三个环圈显示
	average_data = {"so2": 0, "no2": 0, "pm10": 0, "co": 0, "o3": 0, "pm25": 0}
	for data in datas_list:
		average_data["so2"] += data["so2"]
		average_data["no2"] += data["no2"]
		average_data["pm10"] += data["pm10"]
		average_data["co"] += data["co"]
		average_data["o3"] += data["o3"]
		average_data["pm25"] += data["pm25"]
	if len(datas_list) != 0:
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
	else:
		average_data["AQI_1"] = u"无数据"
		average_data["Main_Pollute_1"] = u"无数据"
		average_data["AQI_info_1"] = u"无数据"
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