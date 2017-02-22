# coding=utf-8
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta
from EMP import settings
from django.core.mail import send_mail
from app.views.utils.mySqlUtils import MySQL
from app.models import Sensor, SensorConfigParameter, SensorDatabaseConfig, Project

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
