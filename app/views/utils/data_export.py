# coding=utf-8
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from mySqlUtils import MySQL
from datetime import datetime, timedelta
from variables import transform_factor
from EMP import settings
from django.core.mail import send_mail

# 导出数据
@csrf_exempt
def historical_device_data_export(request):
	if request.method == "GET":
		device_list = []
		for device in range(10):
			tmp = {}
			tmp["id"] = device["NodeNO"]
			# tmp["id"] = device
			tmp["name"] = device["Description"]
			# tmp["name"] = "创业园"
			tmp["address"] = device["InstallationAddress"]
			# tmp["address"] = "电子信息产业园"
			tmp["install_time"] = str(device["SetTime"])
			# tmp["install_time"] = "2017-01-07 12:23:23"
			device_list.append(tmp)
		return render(request, "app/historical_device_data_export.html", {
			"device_list": device_list,
		})
	else:
		return HttpResponse("success")


def historical_device_data_export_function(request, device_id):

	data_date = request.GET.get("data_date", None)
	print data_date
	if data_date is None:
		today = datetime.today()
		data_date = datetime(today.year, today.month, today.day, 0, 0, 0)
		data_date = datetime.strftime(data_date, "%Y-%m-%d %H:%M:%S")

	# device_id = 1
	# data_date = "2017-01-20"

	start_time = datetime.strptime(data_date, "%Y-%m-%d")
	end_time = start_time + timedelta(days=1)
	start_time_str = datetime.strftime(start_time, "%Y-%m-%d %H:%M:%S")
	end_time_str = datetime.strftime(end_time, "%Y-%m-%d %H:%M:%S")
	# return HttpResponse("success")
	sql = MySQL()
	sql.connectDB("projectmanagement")
	data = {}
	data["NodeNO"] = {}
	data["NodeNO"]["conn"] = "="
	data["NodeNO"]["val"] = str(device_id)
	device_info_list = sql.get_query("projectnodeinfo", data)
	sql.close_connect()

	'''
	测试数据
	device_info_list = []
	device_tmp = {}
	device_tmp["NodeNO"] = "1"
	device_tmp["Description"] = u"穿越议案"
	device_tmp["InstallationAddress"] = u"竟是科技大"
	device_tmp["SetTime"] = "2017-01-20 12:00:00"
	device_info_list.append(device_tmp)
	'''



	device_info = {}
	for device in device_info_list:
		device_info["id"] = device["NodeNO"]
		device_info["name"] = device["Description"]
		device_info["address"] = device["InstallationAddress"]
		device_info["install_time"] = str(device["SetTime"])

	sql.connectDB("jssf")


	data = {}
	data[u"项目内节点编号"] = {}
	data[u"项目内节点编号"]["conn"] = "="
	data[u"项目内节点编号"]["val"] = str(device_id)

	data[u"紧缩型时间传感器_实时时间"] = {}
	data[u"紧缩型时间传感器_实时时间"]["conn"] = ">"
	data[u"紧缩型时间传感器_实时时间"]["val"] = str(start_time_str)

	data[u"紧缩型时间传感器_实时时间"] = {}
	data[u"紧缩型时间传感器_实时时间"]["conn"] = "<"
	data[u"紧缩型时间传感器_实时时间"]["val"] = str(end_time_str)

	datas = sql.get_query(u"大气六参数", data, None, u"紧缩型时间传感器_实时时间")
	sql.close_connect()
	# datas.reverse()


	'''
	测试数据
	datas = []
	ap = {}
	ap["SO2_SO2"] = 100
	ap["NO2_NO2"] = 11
	ap["CO_CO"] = 123
	ap["O3_O3"] = 3
	ap["PM2_5_PM2_5"] = 4
	ap["PM10_PM10"] = 4
	ap[u"项目内节点编号"] = 4
	ap[u"紧缩型时间传感器_实时时间"] = "2017-01-20 12:00:00"
	datas.append(ap)
	'''

	datas_list_briage = []
	for data in datas:
		tmp = {}
		try:
			tmp["so2"] = round(float(data["SO2_SO2"]) * transform_factor["so2"],3)
		except:
			tmp["so2"] = data["SO2_SO2"]
		try:
			tmp["no2"] = round(float(data["NO2_NO2"]) * transform_factor["no2"],3)
		except:
			tmp["no2"] = data["NO2_NO2"]
		try:
			tmp["co"] = round(float(data["CO_CO"]) * transform_factor["co"],3)
		except:
			tmp["co"] = data["CO_CO"]
		try:
			tmp["o3"] = round(float(data["O3_O3"]) * transform_factor["o3"],3)
		except:
			tmp["o3"] = data["O3_O3"]
		tmp["pm25"] = data["PM2_5_PM2_5"]
		tmp["pm10"] = data["PM10_PM10"]
		tmp["device_id"] = data[u"项目内节点编号"]
		tmp["time"] = str(data[u"紧缩型时间传感器_实时时间"])
		datas_list_briage.append(tmp)
	datas = datas_list_briage
	# 计算小时日平均数据
	# 计算思路：从1点开始，依次使用当前时间减去一个小时的时间作为起点，当前时间作为终点，获取中间时刻的数据加和求平均
	calculate_result = {}
	factors = ["so2", "no2", "pm10", "co", "o3", "pm25"]
	for i in range(1, 25):
		calculate_result[str(i)] = {}
		int_i = int(i)
		end_time_t = start_time + timedelta(hours=int_i)
		start_time_t = end_time_t - timedelta(hours=1)
		for factor in factors:
			factor_sum = 0
			cnt = 0
			for data in datas:
				if start_time_t <= datetime.strptime(data["time"], "%Y-%m-%d %H:%M:%S") < end_time_t:
					factor_sum += data[factor]
					cnt += 1
				# elif datetime.strptime(data["time"], "%Y-%m-%d %H:%M:%S") > end_time:
				# 	break
			try:
				calculate_result[str(i)][factor] = round(float(factor_sum / cnt), 3)
			except ZeroDivisionError:
				calculate_result[str(i)][factor] = "无数据"
	# print calculate_result
	# 写入excel文件
	try:
		import xlwt
		import random
		workbook = xlwt.Workbook(encoding='utf-8')# 创建工作簿
		mysheet = workbook.add_sheet(device_info["name"] + str(data_date) + u'1小时平均数据')# 创建工作页
		cols = 7 #每行的列
		cols_name = ['时间','O3平均值(ug/m3)','CO平均值(mg/m3)','SO2平均值(ug/m3)','NO2平均值(ug/m3)','PM2.5平均值(ug/m3)','PM10平均值(ug/m3)']#表头名
		for c in range(len(cols_name)):
			mysheet.write(0, c, cols_name[c])

		factors = ["o3", "co", "so2", "no2", "pm25", "pm10"]
		for r in range(0, 24):#对行进行遍历
			mysheet.write(r + 1, 0, str(r+1) + "点")
			for c in range(len(factors)): #对列进行遍历
				mysheet.write(r+1, c + 1, calculate_result[str(r+1)][factors[c]])

		response = HttpResponse(content_type='application/vnd.ms-excel')# 这里响应对象获得了一个特殊的mime类型,告诉浏览器这是个excel文件不是html
		response['Content-Disposition'] = 'attachment; filename=reportdata.xls'# 这里响应对象获得了附加的Content-Disposition协议头,它含有excel文件的名称,文件名随意,当浏览器访问它时,会以"另存为"对话框中使用它.
		workbook.save(response)
		return response
	except Exception as e:
		print(str(e))
		subject = u"导出数据失败通知"
		text_content = u"导出数据失败通知" + str(e)
		from_email = settings.EMAIL_HOST_USER
		to = "929034478@qq.com"
		try:
			send_mail(subject, text_content, from_email, [to], fail_silently=False)
		except Exception as e:
			pass
		return HttpResponse("导出失败，请联系系统管理员")