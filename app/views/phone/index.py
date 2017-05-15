# coding=utf-8
from datetime import datetime, timedelta

from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from app.models import Adminer
from app.views.objects.AqiParameter import AqiParameter
from app.views.utils.mySqlUtils import MySQL
transform_factor = {"so2": 2949.276785714286, "o3": 2142.7767857142856, "co": 1.2504464285714287, "no2": 2054.017857142857}
import json


def index(request, device_id):
	try:
		adminer = Adminer.objects.get(username=request.session["username"])
	except:
		return HttpResponseRedirect("/app/user/login/")
	try:
		adminer_node = adminer.admin_node.split(',')
		if unicode(device_id) not in adminer_node:
			device_id = int(adminer_node[0])
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
			adminer_node = int(adminer.admin_node.split(',')[0])
			device_id = adminer_node
			sql = MySQL()
			sql.connectDB("projectmanagement")
			data = {}
			data["ProjectID"] = {}
			data["ProjectID"]["conn"] = "="
			data["ProjectID"]["val"] = str(device_id)
			device = sql.get_query("projectnodeinfo", data)[0]
			sql.close_connect()
		except:
			device = {}
			return render(request, "phone/index.html", {
				"device_name": {},
				"device_list": {},
				"device_info": {},
				"today_data": {},
			})
	print(device)
	# 获取ID对应的站点
	device_tmp = {}
	device_tmp["id"] = device["NodeNO"]
	device_tmp["name"] = device["Description"]
	device_tmp["address"] = device["InstallationAddress"]
	device_tmp["longitude"] = "117.5436320000"
	device_tmp["latitude"] = "30.7078830000"
	device_tmp["install_time"] = device["SetTime"]
	device = device_tmp
	# 获取ID对应的设备的名称
	device_name = device["name"]
	# 获取ID对应的设备的当前天气状况
	NOW = datetime.today()
	start = datetime(NOW.year, NOW.month, NOW.day, 0, 0, 0) - timedelta(days=1)
	sql = MySQL()
	sql.connectDB("jssf")
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
		tmp["Temperature"] = data["Temperature"]
		tmp["Pressure"] = data["Pressure"]
		tmp["Humidity"] = data["Humidity"]
		tmp["device_id"] = data[u"项目内节点编号"]
		tmp["time"] = str(data[u"紧缩型时间传感器_实时时间"])
		tmp["name"] = device["name"]
		datas_list_briage.append(tmp)
	datas_list = datas_list_briage
	print datas_list
	device_info = {"aqi": "无数据", "level":"无数据", "so2": "无数据", "no2": "无数据", "pm10": "无数据", "co": "无数据",
				 "o3": "无数据", "pm25": "无数据", "reference":"无数据", "results":"无数据"}
	try:
		device_info = datas_list[len(datas_list)-1]
		try:
			calculator = AqiParameter()
			calculator.get_1_aqi(device_info)
			device_info["aqi"] = calculator.AQI_1
			device_info["reference"] = calculator.AQI_info_1
			device_info["results"] = calculator.AQI_info_1
			device_info["level"] = calculator.AQI_info_1
		except Exception as e:
			print(str(e))
			device_info["aqi"] = "无数据"
			device_info["reference"] = "无数据"
			device_info["results"] = "无数据"
			device_info["level"] = "无数据"
	except Exception as e:
		print(str(e))
	# device_info = {
	# 	"aqi": 123,
	# 	"level": 1,
	# 	"pm25": 12,
	# 	"pm10": 50,
	# 	"o3": 1,
	# 	"so2": 3.2,
	# 	"no2": 5,
	# 	"co": 1.2,
	# 	"reference": "空气质量令人满意，基本无空气污染",
	# 	"results": "各类人群可正常活动",
	# }

	# 获取当前账户管理的节点列表
	sql = MySQL()
	sql.connectDB("projectmanagement")
	data = {}
	data["ProjectID"] = {}
	data["ProjectID"]["conn"] = "="
	data["ProjectID"]["val"] = str(1)
	device_list = sql.get_query("projectnodeinfo", data, None)
	sql.close_connect()
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


	today_data = {}
	# today_data["time"] = [1,2,3,4,5,6,7,8,9,10,11,12]
	# today_data["pm25"] = [20,20,30,15,25,6,17,28,19,20,21,22]
	# today_data["pm10"] = [30,30,40,25,35,60,27,38,29,30,31,32]
	# today_data["so2"] = [2,2,3,15,5,6,7,2,1,2,2,2]
	# today_data["no2"] = [20,20,30,15,25,6,17,28,19,20,21,22]
	# today_data["o3"] = [30,20,30,5,25,6,17,8,19,20,1,22]
	# today_data["co"] = [20,20,0,1,25,6,7,2,19,2,21,2]


	# 获取当前设备今天采集的数据，小时级别
	twelve_data_hour = []
	twelve_data_data = {"so2": [], "no2": [], "pm10": [], "co": [], "o3": [], "pm25": []}
	factors = ["so2", "no2", "pm10", "co", "o3", "pm25"]
	for idx, data in enumerate(datas_list):
		twelve_data_hour.append(data["time"])
		for factor in factors:
			try:
				tmp = 0
				cnt = 0
				for i in range(0, 5):
					try:
						tmp += float(datas_list[idx + i][factor])
						cnt += 1
					except:
						pass
				twelve_data_data[factor].append(round(float(tmp / cnt), 3))
			except:
				pass
	today_data["time"] = twelve_data_hour
	today_data["data"] = twelve_data_data

	return render(request, "phone/index.html", {
		"device_name": device_name,
		"device_list": device_list,
		"device_info": device_info,
		"today_data": today_data,
	})


def map(request):
	try:
		adminer = Adminer.objects.get(username=request.session["username"])
	except:
		return HttpResponseRedirect("/app/user/login/")
	try:
		sql = MySQL()
		sql.connectDB("projectmanagement")
		data = {}
		data["ProjectID"] = {}
		data["ProjectID"]["conn"] = "="
		data["ProjectID"]["val"] = str(1)
		device_list = sql.get_query("projectnodeinfo", data, None)
		sql.close_connect()
		longitude_dic = {
			"1": {"name": "齐山医药", "val": 117.5396850000},
			"2": {"name": "赛威机械", "val": 117.5419160000000},
			"3": {"name": "创业园", "val": 117.5379210000000},
			"4": {"name": "太平鸟", "val": 117.5598140000000},
			"5": {"name": "池州港", "val": 117.5641380000},
			"6": {"name": "6号节点", "val": 117.5436320000000},
			"7": {"name": "望华楼", "val": 117.5472020000000},
			"8": {"name": "老干部局", "val": 117.4914460000000},
			"9": {"name": "创业园2", "val": 117.5379220000000},
			"10": {"name": "帽式01", "val": 117.5436320000000},
			"11": {"name": "帽式02", "val": 117.5436320000000},
			"12": {"name": "帽式03", "val": 117.5436320000000},
			"13": {"name": "帽式04", "val": 117.5436320000000},
			"14": {"name": "帽式04", "val": 117.5436320000000},
			"15": {"name": "帽式04", "val": 117.5436320000000},
			"16": {"name": "帽式04", "val": 117.5436320000000},
			"17": {"name": "帽式04", "val": 117.5436320000000},
			"18": {"name": "帽式04", "val": 117.5436320000000},
			"19": {"name": "帽式04", "val": 117.5436320000000},
			"20": {"name": "帽式04", "val": 117.5436320000000},
			"21": {"name": "帽式04", "val": 117.5436320000000},
			"22": {"name": "帽式04", "val": 117.5436320000000},
			"23": {"name": "帽式04", "val": 117.5436320000000},
			"24": {"name": "帽式04", "val": 117.5436320000000},
		}
		latitude_dic = {
			"1": {"name": "齐山医药", "val": 30.7137780000},
			"2": {"name": "赛威机械", "val": 30.703908000000000},
			"3": {"name": "创业园", "val": 30.691674000000000},
			"4": {"name": "太平鸟", "val": 30.705204000000000},
			"5": {"name": "池州港", "val": 30.7393260000},
			"6": {"name": "6号节点", "val": 30.707883000000000},
			"7": {"name": "望华楼", "val": 30.665855000000000},
			"8": {"name": "老干部局", "val": 30.649073000000000},
			"9": {"name": "创业园2", "val": 30.691675000000000},
			"10": {"name": "帽式01", "val": 30.707883000000000},
			"11": {"name": "帽式02", "val": 30.707883000000000},
			"12": {"name": "帽式03", "val": 30.707883000000000},
			"13": {"name": "帽式04", "val": 30.707883000000000},
			"14": {"name": "帽式04", "val": 30.707883000000000},
			"15": {"name": "帽式04", "val": 30.707883000000000},
			"16": {"name": "帽式04", "val": 30.707883000000000},
			"17": {"name": "帽式04", "val": 30.707883000000000},
			"18": {"name": "帽式04", "val": 30.707883000000000},
			"19": {"name": "帽式04", "val": 30.707883000000000},
			"20": {"name": "帽式04", "val": 30.707883000000000},
			"21": {"name": "帽式04", "val": 30.707883000000000},
			"22": {"name": "帽式04", "val": 30.707883000000000},
			"23": {"name": "帽式04", "val": 30.707883000000000},
			"24": {"name": "帽式04", "val": 30.707883000000000},
		}
		device_list_briage = []
		admin_ndoe_list = adminer.admin_node.split(',')
		for device_t in device_list:
			tmp = {}
			tmp["name"] = device_t["Description"]
			tmp["id"] = device_t["NodeNO"]
			tmp["address"] = device_t["InstallationAddress"]
			try:
				tmp["longitude"] = longitude_dic[str(tmp["id"])]["val"]
				tmp["latitude"] = latitude_dic[str(tmp["id"])]["val"]
			except:
				tmp["longitude"] = "117.5436320000000"
				tmp["latitude"] = "30.707883000000000"
			tmp["install_time"] = device_t["SetTime"]
			if unicode(tmp["id"]) in admin_ndoe_list:
				device_list_briage.append(tmp)
		device_list = device_list_briage
		# sql.connectDB("jssf")
		# datas = sql.get_query(u"大气六参数", None, None, u"紧缩型时间传感器_实时时间")
		# datas.reverse()
		# sql.close_connect()
		# datas_list_briage = []
		# for device in device_list:
		# 	flag = 0
		# 	for data in datas:
		# 		tmp = {}
		# 		try:
		# 			tmp["so2"] = round(float(data["SO2_SO2"]) * transform_factor["so2"], 3)
		# 		except:
		# 			tmp["so2"] = data["SO2_SO2"]
		# 		try:
		# 			tmp["no2"] = round(float(data["NO2_NO2"]) * transform_factor["no2"], 3)
		# 		except:
		# 			tmp["no2"] = data["NO2_NO2"]
		# 		try:
		# 			tmp["pm10"] = data["PM10_PM10"]
		# 		except:
		# 			tmp["pm10"] = data["PM10_PM10"]
		# 		try:
		# 			tmp["co"] = round(float(data["CO_CO"]) * transform_factor["co"], 3)
		# 		except:
		# 			tmp["co"] = data["CO_CO"]
		# 		try:
		# 			tmp["o3"] = round(float(data["O3_O3"]) * transform_factor["o3"], 3)
		# 		except:
		# 			tmp["o3"] = data["O3_O3"]
		# 		tmp["pm25"] = data["PM2_5_PM2_5"]
		# 		tmp["device_id"] = data[u"项目内节点编号"]
		# 		tmp["time"] = str(data[u"紧缩型时间传感器_实时时间"])
		# 		if device["id"] == tmp["device_id"]:
		# 			print(device)
		# 			try:
		# 				device["latest_time"] = str(tmp["time"])
		# 				aqi = AqiParameter()
		# 				aqi.get_1_aqi(tmp)
		# 				device["AQI"] = aqi.AQI_1
		# 				device["pm25"] = tmp["pm25"]
		# 				device["so2"] = tmp["so2"]
		# 				device["pm10"] = tmp["pm10"]
		# 				flag = 1
		# 			except Exception as e:
		# 				print(str(e))
		# 			break
		# 	if flag == 0:
		# 		device["AQI"] = u"无数据"
		# 		device["pm25"] = u"无数据"
		# 		device["so2"] = u"无数据"
		# 		device["pm10"] = u"无数据"
		# print(device_list)
	except Exception as e:
		print(str(e))
		device_list = []
	return render(request, "phone/map.html", {
		"device_list": json.dumps(device_list),
	})


def ranking(request):
	try:
		adminer = Adminer.objects.get(username=request.session["username"])
	except:
		return HttpResponseRedirect("/app/user/login/")
	sql = MySQL()
	sql.connectDB("projectmanagement")
	data = {}
	data["ProjectID"] = {}
	data["ProjectID"]["conn"] = "="
	data["ProjectID"]["val"] = str(1)
	device_list = sql.get_query("projectnodeinfo", data, None)
	sql.close_connect()
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


	# 获取每个站点的最新数据

	# 获取今日每个站点采集的所有数据
	sql.connectDB("jssf")
	NOW = datetime.today()
	start = datetime(NOW.year, NOW.month, NOW.day, 0, 0, 0)
	data = {}
	data[u"紧缩型时间传感器_实时时间"] = {}
	data[u"紧缩型时间传感器_实时时间"]["conn"] = ">"
	data[u"紧缩型时间传感器_实时时间"]["val"] = start.strftime("%Y-%m-%d %H:%M:%S")
	datas = sql.get_query(u"大气六参数", data, None, u"紧缩型时间传感器_实时时间")
	datas.reverse()
	sql.close_connect()

	transform_datas = []
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
		transform_datas.append(tmp)

	for device in device_list:
		flag = 0
		for data in transform_datas:
			if device["id"] == data["device_id"]:
				try:
					device["latest_time"] = str(data["time"])
					device["pm25"] = data["pm25"]
					device["pm10"] = data["pm10"]
					device["so2"] = data["so2"]
					device["no2"] = data["no2"]
					device["co"] = data["co"]
					device["o3"] = data["o3"]
					flag = 1
				except Exception as e:
					print(str(e))
				break
		if flag == 0:
			device["pm25"] = u"无数据"
			device["pm10"] = u"无数据"
			device["so2"] = u"无数据"
			device["no2"] = u"无数据"
			device["co"] = u"无数据"
			device["o3"] = u"无数据"

	for device in device_list:
		aqi = AqiParameter()
		try:
			aqi.get_1_aqi(device)
			device["AQI"] = aqi.AQI_1
			device["level"] = aqi.AQI_info_1["level_no"]
			if device["pm25"] is None:
				device["pm25"] = u"无数据"
			if device["pm10"] is None:
				device["pm10"] = u"无数据"
			if device["so2"] is None:
				device["so2"] = u"无数据"
			if device["no2"] is None:
				device["no2"] = u"无数据"
			if device["co"] is None:
				device["co"] = u"无数据"
			if device["o3"] is None:
				device["o3"] = u"无数据"
		except:
			device["AQI"] = u"无数据"
			device["level"] = 6
	# print(device_list)
	aqi_list  = sorted(device_list, key=lambda e: e.__getitem__('AQI'))
	pm25_list  = sorted(device_list, key=lambda e: e.__getitem__('pm25'))
	pm10_list  = sorted(device_list, key=lambda e: e.__getitem__('pm10'))
	so2_list  = sorted(device_list, key=lambda e: e.__getitem__('so2'))
	no2_list  = sorted(device_list, key=lambda e: e.__getitem__('no2'))
	co_list  = sorted(device_list, key=lambda e: e.__getitem__('co'))
	o3_list  = sorted(device_list, key=lambda e: e.__getitem__('o3'))
	# return HttpResponse(aqi_list)
	# aqi_list = [
	# 	{"name": "1", "AQI":25, "level":1},
	# 	{"name": "2", "AQI":25, "level":1},
	# 	{"name": "3", "AQI":25, "level":1},
	# 	{"name": "4", "AQI":25, "level":1},
	# 	{"name": "5", "AQI":25, "level":1},
	# ]
	# pm25_list = [
	# 	{"name": "1", "pm25": 120, "level":2},
	# 	{"name": "2", "pm25": 120, "level":3},
	# 	{"name": "3", "pm25": 120, "level":3},
	# 	{"name": "4", "pm25": 120, "level":4},
	# 	{"name": "5", "pm25": 120, "level":5},
	# ]
	# pm10_list = []
	# so2_list = []
	# no2_list = []
	# co_list = []
	# o3_list = []
	return render(request, "phone/ranking.html", {
		"aqi_list":aqi_list,
		"pm25_list":pm25_list,
		"pm10_list":pm10_list,
		"so2_list":so2_list,
		"no2_list":no2_list,
		"co_list":co_list,
		"o3_list":o3_list,
	})