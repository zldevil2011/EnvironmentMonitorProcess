# coding=utf-8
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from app.models import User, Adminer
from django.contrib.auth.hashers import  check_password, make_password
from app.views.utils.mySqlUtils import MySQL
transform_factor = {"so2": 2949.276785714286, "o3": 2142.7767857142856, "co": 1.2504464285714287, "no2": 2054.017857142857}


@csrf_exempt
def login(request):
	if request.method == "GET":
		return render(request, "phone/login.html", {
		})
	else:
		username = request.POST.get("username")
		password = request.POST.get("password")
		print username, password
		try:
			user = User.objects.get(username=username)
			print check_password(password, user.password)
			if check_password(password, user.password):
				adminer = Adminer.objects.get(user=user)
				request.session["username"] = username
				request.session.set_expiry(0)
				return HttpResponse("success")
			else:
				return HttpResponse("error")
		except:
			return HttpResponse("error")


def logout(request):
	del request.session['username']
	return render(request, "phone/logout.html", {})


def information(request):
	try:
		adminer = Adminer.objects.get(username=request.session["username"])
	except:
		return HttpResponseRedirect("/app/user/login/")

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
	username = adminer.username
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
	return render(request, "phone/information.html", {
		"device_list":device_list,
		"username": username,
	})


@csrf_exempt
def warning_list(request):
	# try:
	# 	adminer = Adminer.objects.get(username=request.session["username"])
	# except:
	# 	return HttpResponseRedirect("/app/user/login/")
	try:
		user_id = int(request.GET.get("user_id"))
	except:
		return HttpResponse("暂时没有数据")
	return render(request, "phone/user_warning_list.html", {
		"user_id":user_id,
	})