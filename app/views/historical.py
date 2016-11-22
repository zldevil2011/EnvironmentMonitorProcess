# coding=utf-8
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from dss.Serializer import serializer
import json
from objects.AqiParameter import AqiParameter


def historical_device(request):
	device_list = [
		{"id": 1, "name": u"京师方圆", "address" : u"凤凰大道", "longitude": 117.2944, "latitude": 30.4127, "latest_time":"2016-11-22 12:00:00", "install_time": "2016-11-12 12:00:00"},
		{"id": 2, "name": u"清风大道路", "address" : u"新城区", "longitude": 117.2944, "latitude": 30.4027, "latest_time":"2016-11-22 12:00:00", "install_time": "2016-11-10 12:00:00"},
	]
	device_data = [
		{"name": u"京师方圆", "so2": 32, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 158,"time": "2016-11-12 12:00:00"},
		{"name": u"清风大道路", "so2": 33, "no2": 20, "pm10": 20, "co": 2, "o3": 12, "pm25": 12,"time": "2016-11-12 12:00:00"}
	]
	for device in device_list:
		for data in device_data:
			if data["name"] == device["name"]:
				aqi = AqiParameter()
				aqi.get_1_aqi(data)
				device["AQI"] = aqi.AQI_1
				device["pm25"] = data["pm25"]
				device["so2"] = data["so2"]
				device["pm10"] = data["pm10"]
				break

	return render(request, "app/historical_device_list.html", {
		"device_list": device_list,
		"device_list_data": json.dumps(device_list),
	})


def historical_data(request):
	return render(request, "app/historical_data.html", {

	})