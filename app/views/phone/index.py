# coding=utf-8
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
transform_factor = {"so2": 2949.276785714286, "o3": 2142.7767857142856, "co": 1.2504464285714287, "no2": 2054.017857142857}


def index(request, device_id):
	# 获取ID对应的站点
	print "okokoko"
	device_list = [{"name":"齐山医药","id":1},{"name":"赛威机械","id":2},
				   {"name":"创业园","id":3},{"name":"太平鸟","id":4},
				   {"name":"池州港","id":5},{"name":"望华楼","id":6},{"name":"老干部局","id":7}]
	device_name = device_list[int(device_id)-1]
	device_info = {
		"aqi":123,
		"level":1,
		"pm25":12,
		"pm10":50,
		"o3":1,
		"so2":3.2,
		"no2":5,
		"co":1.2,
		"reference": "空气质量令人满意，基本无空气污染",
		"results": "各类人群可正常活动",
	}
	today_data = {}
	today_data["time"] = [1,2,3,4,5,6,7,8,9,10,11,12]
	today_data["pm25"] = [20,20,30,15,25,6,17,28,19,20,21,22]
	today_data["pm10"] = [30,30,40,25,35,60,27,38,29,30,31,32]
	today_data["so2"] = [2,2,3,15,5,6,7,2,1,2,2,2]
	today_data["no2"] = [20,20,30,15,25,6,17,28,19,20,21,22]
	today_data["o3"] = [30,20,30,5,25,6,17,8,19,20,1,22]
	today_data["co"] = [20,20,0,1,25,6,7,2,19,2,21,2]
	return render(request, "phone/index.html", {
		"device_name":device_name,
		"device_list":device_list,
		"device_info":device_info,
		"today_data":today_data,
	})