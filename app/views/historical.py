# coding=utf-8
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from dss.Serializer import serializer
import json


def historical_device(request):
	return render(request, "app/historical_device_list.html", {

	})


def historical_data(request):
	return render(request, "app/historical_data.html", {

	})