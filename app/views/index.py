# coding=utf-8
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from dss.Serializer import serializer
import json
from objects.AqiParameter import AqiParameter


def index(request):
	# 获取所有观测点的数据
	datas_list = [
		{"name": u"京师方圆","so2": 32, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 158},
		{"name": u"清风大道路","so2": 33, "no2": 20, "pm10": 20, "co": 2, "o3": 12, "pm25": 12}
	]
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
	# 对所有的观测点进行数据平均计算AQI／PM2.5／首要污染物
	data_real_time = []
	for data in datas_list:
		calculator = AqiParameter()
		calculator.get_1_aqi(data)
		data["AQI_1"] = calculator.AQI_1
		data["Main_Pollute_1"] = calculator.Main_Pollute_1
		data["AQI_info_1"] = calculator.AQI_info_1
		data_real_time.append(data)
		print calculator
	# 计算实时采集数据的均值
	average_data = {"so2": 0, "no2": 0, "pm10": 0, "co": 0, "o3": 0, "pm25": 0}
	for data in datas_list:
		average_data["so2"] += data["so2"]
		average_data["no2"] += data["no2"]
		average_data["pm10"] += data["pm10"]
		average_data["co"] += data["co"]
		average_data["o3"] += data["o3"]
		average_data["pm25"] += data["pm25"]
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
	# 计算最近24小时站点均值

	return render(request, "app/index.html", {
		"average_data": average_data,
		"data_real_time": data_real_time,
	})