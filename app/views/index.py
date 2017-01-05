# coding=utf-8
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from dss.Serializer import serializer
import json
from objects.AqiParameter import AqiParameter
from datetime import datetime, timedelta
from utils.mySqlUtils import MySQL
from django.core.mail import send_mail
from app.models import Adminer
from EMP import settings
import math
from datetime import datetime
transform_factor = {"so2": 2949.276785714286, "o3": 2142.7767857142856, "co": 1.2504464285714287, "no2": 2054.017857142857}


def index(request):
	try:
		adminer = Adminer.objects.get(username=request.session["username"])
	except:
		return HttpResponseRedirect("/user_login/")
	try:
		device_id = request.GET.get("device_id")
		sql = MySQL()
		sql.connectDB("projectmanagement")
		data = {}
		data["NodeNO"] = {}
		data["NodeNO"]["conn"] = "="
		data["NodeNO"]["val"] = str(device_id)
		device = sql.get_query("projectnodeinfo", data)[0]
		sql.close_connect()
	except Exception as e:
		print(str(e))
		try:
			device_id = 1
			sql = MySQL()
			sql.connectDB("projectmanagement")
			data = {}
			data["ProjectID"] = {}
			data["ProjectID"]["conn"] = "="
			data["ProjectID"]["val"] = str(1)
			device = sql.get_query("projectnodeinfo", data)[0]
			sql.close_connect()
		except:
			average_data = {}
			average_data["pm10"] = u"无数据"
			average_data["co"] = u"无数据"
			average_data["o3"] = u"无数据"
			average_data["pm25"] = u"无数据"
			average_data["AQI_1"] = u"无数据"
			average_data["Main_Pollute_1"] = u"无数据"
			average_data["AQI_info_1"] = u"无数据"
			return render(request, "app/index.html", {
				"average_data": average_data,
			})
	try:
		page = int(request.GET.get("page"))
	except Exception as e:
		print str(e)
		page = 1
	print "page", page
	if page < 1:
		return HttpResponseRedirect("/?device_id=" + device_id + "&page=1")

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
	for device_t in device_list:
		tmp = {}
		tmp["name"] = device_t["Description"]
		tmp["id"] = device_t["NodeNO"]
		tmp["address"] = device_t["InstallationAddress"]
		tmp["longitude"] = "117.5436320000"
		tmp["latitude"] = "30.7078830000"
		tmp["install_time"] = device_t["SetTime"]
		device_list_briage.append(tmp)
	device_list = device_list_briage

	device_tmp = {}
	device_tmp["id"] = device["NodeNO"]
	device_tmp["name"] = device["Description"]
	device_tmp["address"] = device["InstallationAddress"]
	device_tmp["longitude"] = "117.5436320000"
	device_tmp["latitude"] = "30.7078830000"
	device_tmp["install_time"] = device["SetTime"]
	device = device_tmp
	NOW = datetime.today()
	start = datetime(NOW.year, NOW.month, NOW.day, 0, 0, 0)
	sql.connectDB("jssf")
	print("xxxxxxxxxxxxxxxxxxxxx")
	print start.strftime("%Y-%m-%d %H:%M:%S")
	data = {}
	data[u"紧缩型时间传感器_实时时间"] = {}
	data[u"紧缩型时间传感器_实时时间"]["conn"] = ">"
	data[u"紧缩型时间传感器_实时时间"]["val"] = start.strftime("%Y-%m-%d %H:%M:%S")
	data[u"项目内节点编号"] = {}
	data[u"项目内节点编号"]["conn"] = "="
	data[u"项目内节点编号"]["val"] = str(device["id"])
	datas = sql.get_query(u"大气六参数", data, None, u"紧缩型时间传感器_实时时间")
	sql.close_connect()
	datas_list_briage = []
	for data in datas:
		tmp = {}
		try:
			tmp["so2"] = round(float(data["SO2_SO2"]) * transform_factor["so2"], 3)
		except:
			tmp["so2"] = data["SO2_SO2"]
		try:
			tmp["no2"] = round(float(data["NO2_NO2"]) * transform_factor["no2"], 3)
		except:
			tmp["no2"] = data["NO2_NO2"]
		try:
			tmp["pm10"] = data["PM10_PM10"]
		except:
			tmp["pm10"] = data["PM10_PM10"]
		try:
			tmp["co"] = round(float(data["CO_CO"]) * transform_factor["co"], 3)
		except:
			tmp["co"] = data["CO_CO"]
		try:
			tmp["o3"] = round(float(data["O3_O3"]) * transform_factor["o3"], 3)
		except:
			tmp["o3"] = data["O3_O3"]
		tmp["pm25"] = data["PM2_5_PM2_5"]
		tmp["device_id"] = data[u"项目内节点编号"]
		tmp["time"] = str(data[u"紧缩型时间传感器_实时时间"])
		tmp["name"] = device["name"]
		datas_list_briage.append(tmp)
	datas_list = datas_list_briage
	datas_list.reverse()
	total_page = int(math.ceil(len(datas_list) / 20.0))
	if total_page < 1:
		total_page = 1
	if page > total_page:
		return HttpResponseRedirect("/?device_id=" + str(device_id) + "&page=" + str(total_page))

	start_num = (page - 1) * 20
	end_num = page * 20
	data_list_20 = datas_list[start_num:end_num]
	for data in datas_list:
		calculator = AqiParameter()
		calculator.get_1_aqi(data)
		data["AQI_1"] = calculator.AQI_1
		data["Main_Pollute_1"] = calculator.Main_Pollute_1
		data["AQI_info_1"] = calculator.AQI_info_1
		# data_collect_time = data["time"]
		# warning_time = datetime.today()
		# warning_time = datetime(warning_time.year, warning_time.month, warning_time.day, warning_time.hour, 0, 0)


	# 计算当前站点实时采集数据的实时数据显示在首页的三个环圈显示
	average_data = {"so2": 0, "no2": 0, "pm10": 0, "co": 0, "o3": 0, "pm25": 0}
	for data in datas_list:
		try:
			average_data["so2"] = data["so2"]
		except:
			average_data["so2"] = 0
		try:
			average_data["no2"] = data["no2"]
		except:
			average_data["no2"] = 0
		try:
			average_data["pm10"] = data["pm10"]
		except:
			average_data["pm10"] = 0
		try:
			average_data["co"] = data["co"]
		except:
			average_data["co"] = 0
		try:
			average_data["o3"] = data["o3"]
		except:
			average_data["o3"] = 0
		try:
			average_data["pm25"] = data["pm25"]
		except:
			average_data["pm25"] = 0
		break
	if len(datas_list) != 0:
		calculator = AqiParameter()
		calculator.get_1_aqi(average_data)
		average_data["AQI_1"] = calculator.AQI_1
		average_data["Main_Pollute_1"] = calculator.Main_Pollute_1
		average_data["AQI_info_1"] = calculator.AQI_info_1
		if int(calculator.AQI_1) >= 450:
			try:
				pre_alarm_time = request.GET.get("pre_alarm_time")
				pre_alarm_time = datetime.strptime(pre_alarm_time, "%Y-%m-%d %H:%M:%S")
			except:
				pre_alarm_time = datetime.strptime("1997-07-01 00:00:00", "%Y-%m-%d %H:%M:%S")
			alarm_now = datetime.strptime(data["time"], "%Y-%m-%d %H:%M:%S")
			if alarm_now > pre_alarm_time:
				subject = u"污染指数通知"
				text_content = u"观测设备" + data["name"] + u"在" + str(data["time"]) + u"AQI值为" + str(calculator.AQI_1) + u",污染程度:" + unicode(calculator.AQI_info_1["classification"])
				from_email = settings.EMAIL_HOST_USER
				to = "929034478@qq.com"
				try:
					send_mail(subject, text_content, from_email, [to], fail_silently=False)
				except Exception as e:
					pass
				pre_alarm_time = datetime.strftime(alarm_now, "%Y-%m-%d %H:%M:%S")
			else:
				pre_alarm_time = datetime.strftime(pre_alarm_time, "%Y-%m-%d %H:%M:%S")
		else:
			pre_alarm_time = ""
	else:
		average_data["AQI_1"] = u"无数据"
		average_data["Main_Pollute_1"] = u"无数据"
		average_data["AQI_info_1"] = u"无数据"
	# 计算显示当天的采集数据曲线图数据
	datas_list_today = datas_list
	twelve_data = {}
	twelve_data_hour = []
	twelve_data_data = {"so2":[], "no2":[], "pm10":[], "co":[], "o3":[], "pm25":[]}
	factors = ["so2", "no2", "pm10", "co", "o3", "pm25"]
	for data in datas_list_today:
		twelve_data_hour.append(data["time"])
		for factor in factors:
			try:
				twelve_data_data[factor].append(float(data[factor]))
			except:
				pass
				# twelve_data_data[factor].append("null")
	twelve_data["twelve_data_hour"] = twelve_data_hour
	twelve_data["twelve_data_data"] = twelve_data_data
	# 参数
	try:
		parameter = request.GET.get("parameter", "PM10")
	except:
		parameter = "PM10"
	return render(request, "app/index.html", {
		# "pre_alarm_time": pre_alarm_time,
		"twelve_data": twelve_data,
		"average_data": average_data,
		"data_real_time": data_list_20,
		"device_list": device_list,
		"page": page,
		"total_page": total_page,
		"device": device,
		"parameter": parameter,
	})


def index_48(request):
	try:
		adminer = Adminer.objects.get(username=request.session["username"])
	except:
		return HttpResponseRedirect("/user_login/")
	try:
		device_id = request.GET.get("device_id")
		sql = MySQL()
		sql.connectDB("projectmanagement")
		data = {}
		data["NodeNO"] = {}
		data["NodeNO"]["conn"] = "="
		data["NodeNO"]["val"] = str(device_id)
		device = sql.get_query("projectnodeinfo", data)[0]
		sql.close_connect()
	except Exception as e:
		print(str(e))
		try:
			device_id = 1
			sql = MySQL()
			sql.connectDB("projectmanagement")
			data = {}
			data["ProjectID"] = {}
			data["ProjectID"]["conn"] = "="
			data["ProjectID"]["val"] = str(1)
			device = sql.get_query("projectnodeinfo", data)[0]
			sql.close_connect()
		except:
			average_data = {}
			average_data["pm10"] = u"无数据"
			average_data["co"] = u"无数据"
			average_data["o3"] = u"无数据"
			average_data["pm25"] = u"无数据"
			average_data["AQI_1"] = u"无数据"
			average_data["Main_Pollute_1"] = u"无数据"
			average_data["AQI_info_1"] = u"无数据"
			return render(request, "app/index.html", {
				"average_data": average_data,
			})
	try:
		page = int(request.GET.get("page"))
	except Exception as e:
		print str(e)
		page = 1
	print "page", page
	if page < 1:
		return HttpResponseRedirect("/?device_id=" + device_id + "&page=1")

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
	for device_t in device_list:
		tmp = {}
		tmp["name"] = device_t["Description"]
		tmp["id"] = device_t["NodeNO"]
		tmp["address"] = device_t["InstallationAddress"]
		tmp["longitude"] = "117.5436320000"
		tmp["latitude"] = "30.7078830000"
		tmp["install_time"] = device_t["SetTime"]
		device_list_briage.append(tmp)
	device_list = device_list_briage

	device_tmp = {}
	device_tmp["id"] = device["NodeNO"]
	device_tmp["name"] = device["Description"]
	device_tmp["address"] = device["InstallationAddress"]
	device_tmp["longitude"] = "117.5436320000"
	device_tmp["latitude"] = "30.7078830000"
	device_tmp["install_time"] = device["SetTime"]
	device = device_tmp
	NOW = datetime.today()
	start = datetime(NOW.year, NOW.month, NOW.day, 0, 0, 0)
	sql.connectDB("jssf")
	print("xxxxxxxxxxxxxxxxxxxxx")
	print start.strftime("%Y-%m-%d %H:%M:%S")
	data = {}
	data[u"紧缩型时间传感器_实时时间"] = {}
	data[u"紧缩型时间传感器_实时时间"]["conn"] = ">"
	data[u"紧缩型时间传感器_实时时间"]["val"] = start.strftime("%Y-%m-%d %H:%M:%S")
	data[u"项目内节点编号"] = {}
	data[u"项目内节点编号"]["conn"] = "="
	data[u"项目内节点编号"]["val"] = str(device["id"])
	datas = sql.get_query(u"大气六参数", data, None, u"紧缩型时间传感器_实时时间")
	sql.close_connect()
	datas_list_briage = []
	for data in datas:
		tmp = {}
		try:
			tmp["so2"] = round(float(data["SO2_SO2"]) * transform_factor["so2"], 3)
		except:
			tmp["so2"] = data["SO2_SO2"]
		try:
			tmp["no2"] = round(float(data["NO2_NO2"]) * transform_factor["no2"], 3)
		except:
			tmp["no2"] = data["NO2_NO2"]
		try:
			tmp["pm10"] = data["PM10_PM10"]
		except:
			tmp["pm10"] = data["PM10_PM10"]
		try:
			tmp["co"] = round(float(data["CO_CO"]) * transform_factor["co"], 3)
		except:
			tmp["co"] = data["CO_CO"]
		try:
			tmp["o3"] = round(float(data["O3_O3"]) * transform_factor["o3"], 3)
		except:
			tmp["o3"] = data["O3_O3"]
		tmp["pm25"] = data["PM2_5_PM2_5"]
		tmp["device_id"] = data[u"项目内节点编号"]
		tmp["time"] = str(data[u"紧缩型时间传感器_实时时间"])
		tmp["name"] = device["name"]
		datas_list_briage.append(tmp)
	datas_list = datas_list_briage
	datas_list.reverse()
	total_page = int(math.ceil(len(datas_list) / 20.0))
	if total_page < 1:
		total_page = 1
	if page > total_page:
		return HttpResponseRedirect("/?device_id=" + str(device_id) + "&page=" + str(total_page))

	start_num = (page - 1) * 20
	end_num = page * 20
	data_list_20 = datas_list[start_num:end_num]
	for data in datas_list:
		calculator = AqiParameter()
		calculator.get_1_aqi(data)
		data["AQI_1"] = calculator.AQI_1
		data["Main_Pollute_1"] = calculator.Main_Pollute_1
		data["AQI_info_1"] = calculator.AQI_info_1
		# data_collect_time = data["time"]
		# warning_time = datetime.today()
		# warning_time = datetime(warning_time.year, warning_time.month, warning_time.day, warning_time.hour, 0, 0)


	# 计算当前站点实时采集数据的实时数据显示在首页的三个环圈显示
	average_data = {"so2": 0, "no2": 0, "pm10": 0, "co": 0, "o3": 0, "pm25": 0}
	for data in datas_list:
		try:
			average_data["so2"] = data["so2"]
		except:
			average_data["so2"] = 0
		try:
			average_data["no2"] = data["no2"]
		except:
			average_data["no2"] = 0
		try:
			average_data["pm10"] = data["pm10"]
		except:
			average_data["pm10"] = 0
		try:
			average_data["co"] = data["co"]
		except:
			average_data["co"] = 0
		try:
			average_data["o3"] = data["o3"]
		except:
			average_data["o3"] = 0
		try:
			average_data["pm25"] = data["pm25"]
		except:
			average_data["pm25"] = 0
		break
	if len(datas_list) != 0:
		calculator = AqiParameter()
		calculator.get_1_aqi(average_data)
		average_data["AQI_1"] = calculator.AQI_1
		average_data["Main_Pollute_1"] = calculator.Main_Pollute_1
		average_data["AQI_info_1"] = calculator.AQI_info_1
		if int(calculator.AQI_1) >= 450:
			try:
				pre_alarm_time = request.GET.get("pre_alarm_time")
				pre_alarm_time = datetime.strptime(pre_alarm_time, "%Y-%m-%d %H:%M:%S")
			except:
				pre_alarm_time = datetime.strptime("1997-07-01 00:00:00", "%Y-%m-%d %H:%M:%S")
			alarm_now = datetime.strptime(data["time"], "%Y-%m-%d %H:%M:%S")
			if alarm_now > pre_alarm_time:
				subject = u"污染指数通知"
				text_content = u"观测设备" + data["name"] + u"在" + str(data["time"]) + u"AQI值为" + str(calculator.AQI_1) + u",污染程度:" + unicode(calculator.AQI_info_1["classification"])
				from_email = settings.EMAIL_HOST_USER
				to = "929034478@qq.com"
				try:
					send_mail(subject, text_content, from_email, [to], fail_silently=False)
				except Exception as e:
					pass
				pre_alarm_time = datetime.strftime(alarm_now, "%Y-%m-%d %H:%M:%S")
			else:
				pre_alarm_time = datetime.strftime(pre_alarm_time, "%Y-%m-%d %H:%M:%S")
		else:
			pre_alarm_time = ""
	else:
		average_data["AQI_1"] = u"无数据"
		average_data["Main_Pollute_1"] = u"无数据"
		average_data["AQI_info_1"] = u"无数据"
	# 计算显示当天的采集数据曲线图数据
	datas_list_today = datas_list
	twelve_data = {}
	twelve_data_hour = []
	twelve_data_data = {"so2":[], "no2":[], "pm10":[], "co":[], "o3":[], "pm25":[]}
	factors = ["so2", "no2", "pm10", "co", "o3", "pm25"]
	start_time_0 = datetime(NOW.year, NOW.month, NOW.day, 0, 0, 0)
	twelve_data_hour.append(datetime.strftime(start_time_0, "%Y-%m-%d %H:%M:%S"))
	for i in range(48):
		start_time_0 += timedelta(minutes=30)
		twelve_data_hour.append(datetime.strftime(start_time_0, "%Y-%m-%d %H:%M:%S"))
	print len(twelve_data_hour)
	for end_time in twelve_data_hour:
		end_time = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
		start_time = end_time - timedelta(minutes=30)
		for factor in factors:
			tp = 0
			cnt = 0
			for data in datas_list_today:
				data_time = datetime.strptime(data["time"], "%Y-%m-%d %H:%M:%S")
				if start_time < data_time <= end_time:
					tp += float(data[factor])
					cnt += 1
			try:
				twelve_data_data[factor].append(tp/cnt)
			except:
				pass
	twelve_data["twelve_data_hour"] = twelve_data_hour
	twelve_data["twelve_data_data"] = twelve_data_data
	# 参数
	try:
		parameter = request.GET.get("parameter", "PM10")
	except:
		parameter = "PM10"
	return render(request, "app/index.html", {
		# "pre_alarm_time": pre_alarm_time,
		"twelve_data": twelve_data,
		"average_data": average_data,
		"data_real_time": data_list_20,
		"device_list": device_list,
		"page": page,
		"total_page": total_page,
		"device": device,
		"parameter": parameter,
	})