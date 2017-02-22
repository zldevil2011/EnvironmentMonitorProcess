# coding=utf-8
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta
from EMP import settings
from django.core.mail import send_mail
from app.views.utils.mySqlUtils import MySQL


# 配置首页
@csrf_exempt
def server_index(request):
	# sql = MySQL()
	# sql.connectDB("projectmanagement")
	# data = {}
	# data["ProjectID"] = {}
	# data["ProjectID"]["conn"] = "="
	# data["ProjectID"]["val"] = str(1)
	# devices = sql.get_query("projectnodeinfo", data)
	# sql.close_connect()
	# device_list = []
	# for device in devices:
	# 	tmp = {}
	# 	tmp["id"] = device["NodeNO"]
	# 	tmp["name"] = device["Description"]
	# 	tmp["address"] = device["InstallationAddress"]
	# 	tmp["install_time"] = str(device["SetTime"])
	# 	device_list.append(tmp)
	return render(request, "server/server_index.html",{
		# "device_list": device_list,
	})