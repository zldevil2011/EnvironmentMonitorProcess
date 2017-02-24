# coding=utf-8
import SocketServer
import base64
import hashlib
import socket

import sys
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

from MSP_server.Lora_Receive_thread import ReceiveThread
from MSP_server.main import MSP
from MSP_server.setting import AppEUI
from MSP_server.web_socket_server import Th


@csrf_exempt
def msp_login(request):
	# return HttpResponse("success")
	msp = MSP()
	try:
		msp.get_tcp_sock()
	except Exception as e:
		print(str(e))
		return HttpResponse("error")
	res = msp.join_server()

	if res == 1:
		return HttpResponse("success")
	else:
		return HttpResponse(AppEUI)


@csrf_exempt
def msp_sendto(request):
	msp = MSP()
	try:
		msp.get_tcp_sock()
	except Exception as e:
		print(str(e))
		return HttpResponse("error")
	res = msp.sendto_server("004A770203000002","update paramter", "false")
	if res == 1:
		return HttpResponse("success")
	else:
		return HttpResponse("error")


@csrf_exempt
def msp_logout(request):
	msp = MSP()
	try:
		msp.get_tcp_sock()
	except Exception as e:
		print(str(e))
		return HttpResponse("error")
	res = msp.quit_server()
	if res == 1:
		return HttpResponse("success")
	else:
		return HttpResponse("error")


@csrf_exempt
def msp_receive_data(request):
	msp = MSP()
	try:
		msp.get_tcp_sock()
	except Exception as e:
		print(str(e))
		return HttpResponse("error")
	# res = msp.sendto_cs()


	# log_thread = Th()
	# log_thread.start()

	new_thread = ReceiveThread(1, 1)
	new_thread.start()
	res = 1
	if res == 1:
		return HttpResponse("success")
	else:
		return HttpResponse("error")

@csrf_exempt
def msp_receive_log(request):
	try:
		result = list()
		with open('./' + "receive.log", 'r') as destination:
			line = destination.readline()  # 调用文件的 readline()方法
			while line:
				result.append(line)
				# print line,  # 后面跟 ',' 将忽略换行符
				# print(line, end = '')　　　# 在 Python 3中使用
				line = destination.readline()

		# f.close()
		# f = open('./MSP_server/receive.log', 'r')
		# result = list()
		# for line in f:
		# 	line = f.readline()
		# 	print line
		# 	result.append(line)
		# print result
		# f.close()
	except Exception as e:
		print(str(e))
	return HttpResponse(result)
