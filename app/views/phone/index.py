# coding=utf-8
from datetime import datetime

from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from app.models import Adminer
from app.views.objects.AqiParameter import AqiParameter
from app.views.utils.mySqlUtils import MySQL
transform_factor = {"so2": 2949.276785714286, "o3": 2142.7767857142856, "co": 1.2504464285714287, "no2": 2054.017857142857}

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
	start = datetime(NOW.year, NOW.month, NOW.day, 0, 0, 0)
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
			device_info["reference"] = calculator.AQI_info_1.health
			device_info["results"] = calculator.AQI_info_1.step
			device_info["level"] = calculator.AQI_info_1.level_no
		except Exception as e:
			return HttpResponse(str(e))
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