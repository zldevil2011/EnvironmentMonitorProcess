# coding=utf-8
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta
from EMP import settings
from django.core.mail import send_mail
from app.views.utils.mySqlUtils import MySQL
from app.models import Sensor, SensorConfigParameter, SensorDatabaseConfig, Project, Device
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
	# for i in range(10):
	# 	tmp = {}
	# 	tmp["id"] = random.randint(10,20)
	# 	tmp["name"] = random.randint(10,20)
	# 	tmp["address"] = "InstallationAddress"
	# 	tmp["install_time"] = "2017-12-12 12:12:12"
	# 	device_list.append(tmp)

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
	datas.reverse()
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
	total_page = int(len(datas_list)/100)
	if total_page < 1:
		total_page = 1
	if page > total_page:
		return HttpResponseRedirect("/server_device_data?page=" + str(total_page))
	start_num = (page - 1) * 100
	end_num = page * 100
	datas_list = datas_list[start_num:end_num]
	return render(request, "server/server_device_data.html", {
		"datas_list": datas_list,
		"page": page,
		"total_page": total_page,
	})


@csrf_exempt
def server_device_data_list(request):
	try:
		device_id = int(request.GET.get("device_id"))
		sql = MySQL()
		sql.connectDB("projectmanagement")
		data = {}
		data["NodeNo"] = {}
		data["NodeNo"]["conn"] = "="
		data["NodeNo"]["val"] = str(device_id)
		device = sql.get_query("projectnodeinfo", data)[0]
		sql.close_connect()
	except:
		return HttpResponse("设备不存在")
	device["id"] = device["NodeNO"]
	device["name"] = device["Description"]
	device["address"] = device["InstallationAddress"]
	device["install_time"] = str(device["SetTime"])
	# 获取数据
	sql.connectDB("jssf")
	datas = sql.get_query(u"大气六参数", None, None, u"紧缩型时间传感器_实时时间")
	sql.close_connect()

	datas_list = []
	datas.reverse()
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
		if device["id"] == tmp["device_id"]:
			tmp["name"] = device["name"]
			datas_list.append(tmp)
	try:
		page = int(request.GET.get("page", 1))
		if page < 1:
			return HttpResponseRedirect("/server_device_data_list?page=" + str(1))
	except:
		page = 1
	total_page = int(len(datas_list)/100)
	if total_page < 1:
		total_page = 1
	if page > total_page:
		return HttpResponseRedirect("/server_device_data_list?page=" + str(total_page))
	start_num = (page - 1) * 100
	end_num = page * 100
	datas_list = datas_list[start_num:end_num]
	return render(request, "server/server_device_data.html", {
		"datas_list": datas_list,
		"page": page,
		"total_page": total_page,
	})


@csrf_exempt
def server_device_add(request):
	if request.method == "GET":
		return render(request, "server/server_device_add.html", {

		})
	else:
		try:
			project = Project.objects.get(name = u"大气六参数")
			device_id = request.POST.get("device_id", None)
			name = request.POST.get("name", None)
			address = request.POST.get("address", None)
			install_time = request.POST.get("install_time", None)
			if device_id is None or name is None or address is None or install_time is None:
				return HttpResponse("error")
			install_time = datetime.strptime(install_time, "%Y-%m-%d")

			device = Device()
			device.num = device_id
			device.name = name
			device.address = address
			device.install_time = install_time
			device.project_id = project.pk
			device.save()

			itp = str(install_time)
			itp = itp.replace('-', '/')
			itp_pre = itp.split(' ')[0].split('/')
			if len(itp_pre[1]) == 2 and int(itp_pre[1]) < 10:
				itp_pre[1] = itp_pre[1][1]
			install_time = itp_pre[0] + "/" + itp_pre[1] + "/" + itp_pre[2] + " " + itp.split(' ')[1]

			data = {}
			data["ManagementID"] = str(device_id)
			data["ProjectID"] = str(project.pk)
			data["NodeNO"] = str(device_id)
			data["NodeName"] = str(name)
			data["InstallationAddress"] = str(address)
			data["MathinID"] = str(device_id)
			data["SetTime"] = str(install_time)
			data["Description"] = str(name)
			sql = MySQL()
			sql.connectDB("projectmanagement")
			result = sql.insert_data("projectnodeinfo", data)
			sql.close_connect()
			if result == "success":
				return HttpResponse("success")
			else:
				return HttpResponse("error")
		except Exception as e:
			print(str(e))
			return HttpResponse("error")


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


@csrf_exempt
def server_device_info(request):
	if request.method == "GET":
		try:
			device_id = int(request.GET.get("device_id"))
			# 获取SQLite数据存储的数据
			'''待实现'''
			# 获取Mysql数据库存储的数据
			sql = MySQL()
			sql.connectDB("projectmanagement")
			data = {}
			data["NodeNo"] = {}
			data["NodeNo"]["conn"] = "="
			data["NodeNo"]["val"] = str(device_id)
			device = sql.get_query("projectnodeinfo", data)[0]
			sql.close_connect()
			device["id"] = device["NodeNO"]
			device["name"] = device["Description"]
			device["address"] = device["InstallationAddress"]
			itp = str(device["SetTime"]).split(' ')[0].split('/')
			str_year = itp[0]
			str_month = itp[1]
			str_day = itp[2]
			if len(str_month) < 2:
				str_month = "0" + str_month
			if len(str_day) < 2:
				str_day = "0" + str_day
			device["install_time"] = str_year + "-" + str_month + "-" + str_day

		except Exception as e:
			print(str(e))
			return HttpResponse("设备不存在")
		# device = {}
		# device["id"] = 1
		# device["name"] = "Description"
		# device["address"] = "InstallationAddress"
		# device["install_time"] = str("2016-12-12")[0:10]
		return render(request, "server/server_device_info.html", {
			"device": device,
		})
	else:
		# 更新设备信息
		try:
			device_id = int(request.POST.get("device_id"))
			name = request.POST.get("name", None)
			address = request.POST.get("address", None)
			install_time = request.POST.get("install_time", None)
			print device_id, name, address, install_time
			# return HttpResponse("error")
			if name is None or address is None or install_time is None:
				return HttpResponse("error")
			install_time = datetime.strptime(install_time, "%Y-%m-%d")
			# 更新SQLite数据存储的数据
			'''待实现'''
			device_object = Device.objects.get(num=device_id)
			device_object.name = name
			device_object.address = address
			device_object.install_time = install_time
			device_object.save()

			# 更新Mysql数据库存储的数据
			sql = MySQL()
			sql.connectDB("projectmanagement")
			datas = {}
			datas["NodeName"] = name
			datas["Description"] = name
			datas["InstallationAddress"] = address
			itp = str(install_time)
			itp = itp.replace('-', '/')
			itp_pre = itp.split(' ')[0].split('/')
			if len(itp_pre[1]) == 2 and int(itp_pre[1]) < 10:
				itp_pre[1] = itp_pre[1][1]
			install_time = itp_pre[0] + "/" + itp_pre[1] + "/" + itp_pre[2] + " " + itp.split(' ')[1]
			datas["SetTime"] = str(install_time)
			keys = {}
			keys["NodeNo"] = str(device_id)
			result = sql.update_data("projectnodeinfo", datas, keys)
			sql.close_connect()

			if result == "success":
				return HttpResponse("success")
			else:
				return HttpResponse("error")

		except Exception as e:
			print(str(e))
			return HttpResponse("error")

@csrf_exempt
def server_data_log(request):

	receive_log = list()
	try:
		with open('./' + "receive.log", 'r') as destination:
			line = destination.readline()  # 调用文件的 readline()方法
			while line:
				receive_log.append(line)
				line = destination.readline()
	except:
		pass
	receive_log.reverse()
	receive_log = receive_log[:30]
	return render(request, "server/server_data_log.html", {
		"receive_log": receive_log,
	})


@csrf_exempt
def server_device_eui(request):
	if request.method == "GET":
		project = Project.objects.get(name=u"大气六参数")
		device_list = Device.objects.filter(project_id=project.id)

		return render(request, "server/server_device_eui.html", {
			"device_list": device_list,
		})
	else:
		device_id = request.POST.get("device_id", None)
		deveui = request.POST.get("deveui", None)
		print(device_id)
		print(deveui)
		if device_id is None or deveui is None:
			return HttpResponse("error")
		try:
			device = Device.objects.get(num=int(device_id))
			device.dev_eui = deveui
			device.save()
			return HttpResponse("success")
		except Exception as e:
			print(str(e))
			return HttpResponse("error")

from app.views.utils.listeningData import ReadWarningEventThread, CreateWarningEventThread


def start_listening(request):
	try:
		# read_thread = ReadWarningEventThread()
		# read_thread.start()

		new_thread = CreateWarningEventThread(1,[1], 1)
		new_thread.start()

		res = 1
	except Exception as e:
		res = 0
		print(str(e))
	if res == 1:
		return HttpResponse("success")
	else:
		return HttpResponse("error")
