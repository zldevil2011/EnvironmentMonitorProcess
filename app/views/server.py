# coding=utf-8
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta
from EMP import settings
from django.core.mail import send_mail
from app.views.utils.mySqlUtils import MySQL
from app.models import Sensor, SensorConfigParameter, SensorDatabaseConfig, Project
import random

# 配置首页
@csrf_exempt
def server_index(request):
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
		tmp["install_time"] = str(device["SetTime"])
		device_list.append(tmp)
	return render(request, "server/server_index.html",{
		"device_list": device_list,
	})


@csrf_exempt
def server_device_data(request):
	# 获取设备列表
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
		tmp["install_time"] = str(device["SetTime"])
		device_list.append(tmp)
	# 获取数据
	sql.connectDB("jssf")
	datas = sql.get_query(u"大气六参数", None, None, u"紧缩型时间传感器_实时时间")
	sql.close_connect()

	datas_list = []

	for data in datas:
		tmp = {}
		tmp["so2"] = data["SO2_SO2"]
		tmp["no2"] = data["NO2_NO2"]
		tmp["pm10"] = data["PM10_PM10"]
		tmp["co"] = data["CO_CO"]
		tmp["o3"] = data["O3_O3"]
		tmp["pm25"] = data["PM2_5_PM2_5"]
		tmp["device_id"] = data[u"项目内节点编号"]
		tmp["time"] = str(data[u"紧缩型时间传感器_实时时间"])
		for device in device_list:
			if device["id"] == tmp["device_id"]:
				tmp["name"] = device["name"]
				break
		datas_list.append(tmp)
	# for i in range(10):
	# 	tmp = {}
	# 	tmp["so2"] = random.randint(10,20)
	# 	tmp["no2"] = random.randint(5,20)
	# 	tmp["pm10"] = random.randint(1,20)
	# 	tmp["co"] = random.randint(10,50)
	# 	tmp["o3"] = random.randint(10,201)
	# 	tmp["pm25"] = random.randint(10,30)
	# 	tmp["device_id"] = random.randint(10,20)
	# 	tmp["time"] = "2017-12-12 12:00:00"
	# 	tmp["name"] = "京师方圆"
	# 	datas_list.append(tmp)
	try:
		page = int(request.GET.get("page", 1))
		if page < 1:
			return HttpResponseRedirect("/server_device_data?page=" + str(1))
	except:
		page = 1
	total_page = int(len(datas_list)/30)
	if total_page < 1:
		total_page = 1
	if page > total_page:
		return HttpResponseRedirect("/server_device_data?page=" + str(total_page))
	start_num = (page - 1) * 30
	end_num = page * 30
	datas_list = datas_list[start_num:end_num]
	return render(request, "server/server_device_data.html", {
		"datas_list": datas_list,
		"page": page,
		"total_page": total_page,
	})


@csrf_exempt
def server_device_add(request):
	return render(request, "server/server_device_add.html", {

	})


@csrf_exempt
def server_device_parameter(request):
	project = Project.objects.get(name=u"大气六参数")
	project_sensor_list = SensorConfigParameter.objects.filter(project_id=project.id)
	if request.method == "GET":
		return render(request, "server/server_device_parameter.html", {
			"project_sensor_list":project_sensor_list,
		})
	else:
		parameter_dic = request.POST.get("paramater_data", None)
		print parameter_dic
		try:
			parameter_dic = eval(parameter_dic)
			for k in parameter_dic.keys():
				scp = SensorConfigParameter.objects.get(id = int(k))
				scp.val = float(parameter_dic[k])
				scp.save()
		except Exception as e:
			print(str(e))
			return HttpResponse("error")
		return HttpResponse("success")

@csrf_exempt
def server_project_sensor_config(request):
	if request.method == "GET":
		project = Project.objects.get(name=u"大气六参数")
		project_sensor_object = SensorConfigParameter.objects.filter(project_id=project.id)
		project_sensor = []
		for psc in project_sensor_object:
			project_sensor.append(psc.code)
		project_sensor = Sensor.objects.filter(code__in=project_sensor)
		all_sensor = Sensor.objects.exclude(code__in=project_sensor)

		return render(request, "server/server_project_sensor_config.html", {
			"project_sensor":project_sensor,
			"all_sensor": all_sensor,
		})
	else:
		sensor_list = request.POST.get("sensor_list", None)
		project_name = request.POST.get("project_name", None)
		print(sensor_list)
		if sensor_list is None or project_name is None:
			return HttpResponse("error")
		try:
			sensor_list = sensor_list.split(',')
			project = Project.objects.get(name = project_name)
			project_sensor_object = SensorConfigParameter.objects.filter(project_id=project.id)
			for pso in project_sensor_object:
				if pso.code in sensor_list:
					sensor_list.remove(pso.code)
				else:
					pso.delete()
			for code in sensor_list:
				scp = SensorConfigParameter()
				scp.project_id = project.id
				SENSOR = Sensor.objects.get(code=int(code))
				scp.name = SENSOR.name
				scp.code = int(code)
				scp.val = 1000
				scp.save()

			return HttpResponse("success")
		except Exception as e:
			print(str(e))
			return HttpResponse("error")


@csrf_exempt
def server_sensor_list(request):
	sensor_list = Sensor.objects.all()
	return render(request, "server/server_sensor_list.html", {
		"sensor_list": sensor_list,
	})
