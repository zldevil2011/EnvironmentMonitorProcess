#encoding=utf-8
import threading
import SocketServer
import json
import socket
import ctypes
from app.views.utils.mySqlUtils import MySQL
import time
from datetime import datetime
import time
transform_factor = {"so2": 2949.276785714286, "o3": 2142.7767857142856, "co": 1.2504464285714287, "no2": 2054.017857142857}
from app.models import LatestData, WarningRule, WarningEvent, Adminer
from app.views.objects.AqiParameter import AqiParameter
from dss.Serializer import serializer
from django.core.mail import send_mail
from EMP import settings

class CreateWarningEventThread(threading.Thread):
	def __init__(self, pid, device_id_list):
		threading.Thread.__init__(self)
		self.pid = pid
		self.device_id_list = device_id_list

	def run(self):
		while True:
			# 每5分钟检查一次最新数据是否超过预警值，如果超过新建报警事件
			self.create_warning()
			time.sleep(300)

	def create_warning(self):
		sql = MySQL()
		sql.connectDB("jssf")
		NOW = datetime.today()
		start = datetime(NOW.year, NOW.month, NOW.day, 0, 0, 0)
		data = {}
		data[u"紧缩型时间传感器_实时时间"] = {}
		data[u"紧缩型时间传感器_实时时间"]["conn"] = ">"
		data[u"紧缩型时间传感器_实时时间"]["val"] = start.strftime("%Y-%m-%d %H:%M:%S")
		datas = sql.get_query(u"大气六参数", data, None, u"紧缩型时间传感器_实时时间")
		sql.close_connect()
		datas_list_briage = []
		for data in datas:
			tmp = {}
			try:
				tmp["so2"] = round(float(data["SO2_SO2"]) * transform_factor["so2"], 3)
			except:
				tmp["so2"] = data["SO2_SO2"]
			try:
				tmp["no2"] = round(float(data["NO2_NO2"]) * transform_factor["no2"], 3)
			except:
				tmp["no2"] = data["NO2_NO2"]
			try:
				tmp["pm10"] = data["PM10_PM10"]
			except:
				tmp["pm10"] = data["PM10_PM10"]
			try:
				tmp["co"] = round(float(data["CO_CO"]) * transform_factor["co"], 3)
			except:
				tmp["co"] = data["CO_CO"]
			try:
				tmp["o3"] = round(float(data["O3_O3"]) * transform_factor["o3"], 3)
			except:
				tmp["o3"] = data["O3_O3"]
			tmp["pm25"] = data["PM2_5_PM2_5"]
			tmp["Temperature"] = data["Temperature"]
			tmp["Pressure"] = data["Pressure"]
			tmp["Humidity"] = data["Humidity"]
			tmp["device_id"] = str(data[u"项目内节点编号"])
			tmp["time"] = str(data[u"紧缩型时间传感器_实时时间"])
			try:
				calculator = AqiParameter()
				calculator.get_1_aqi(tmp)
				tmp["aqi"] = calculator.AQI_1
			except Exception as e:
				print(str(e))
				tmp["aqi"] = u"无数据"
			datas_list_briage.append(tmp)
		datas_list = datas_list_briage
		datas_list.reverse()
		latest_data_dic = {}
		pre_data_dic = {}
		for device_id in self.device_id_list:
			latest_data_dic[str(device_id)] = None
			pre_data_dic[str(device_id)] = None
		# 获取当前所有节点的最新数据
		# latest_data_dic是按照现在的设备列表生成的最新的数据列表
		for data in datas_list:
			if latest_data_dic[str(data["device_id"])] is None:
				latest_data_dic[str(data["device_id"])] = data
			elif pre_data_dic[str(data["device_id"])] is None:
				pre_data_dic[str(data["device_id"])] = data
		print latest_data_dic
		for k in latest_data_dic:
			k = latest_data_dic[str(k)]
			k_pre = pre_data_dic[str(k)]
			# 如果存在次新的数据，即k_pre 不等于None
			if k_pre is not None:
				try:
					warning_rule_list = WarningRule.objects.filter(device_id=int(k["device_id"]))
					for warning_rule in warning_rule_list:
						if warning_rule.warning_type == 0:
							# 0代表超过某一个数值就报警
							warning_val = warning_rule.warning_val
							warning_parameter = warning_rule.parameter
							if k[warning_parameter] > warning_val:
								# 超过预定的数值，新建对应的预警实例
								nt = WarningEvent()
								nt.device_id = int(k["device_id"])
								nt.warning_time = datetime.strptime(k["time"], "%Y-%m-%d %H:%M:%S")
								nt.content = k["device_id"] + "号设备" + warning_parameter + "在" + k["time"] + "数值超过预期阈值"
								nt.save()
						elif warning_rule.warning_type == 1:
							# 1代表增长率超过一定数值就报警
							warning_val = warning_rule.warning_val
							warning_parameter = warning_rule.parameter
							pre_val = k_pre[warning_parameter]
							pre_msg = json.dumps(pre_val)
							if k[warning_parameter] > pre_val:
								try:
									rate = (k[warning_parameter] - pre_val) / pre_val
									if rate >= warning_val:
										# 超过预设的百分比，新建对应的预警实例
										nt = WarningEvent()
										nt.device_id = int(k["device_id"])
										nt.warning_time = datetime.strptime(k["time"], "%Y-%m-%d %H:%M:%S")
										nt.content = k["device_id"] + "号设备" + warning_parameter + "在" + k["time"] + "增长率超过预期阈值，达到" + str(rate)
										nt.save()
										subject = u"增长过快通知"
										text_content = nt.content + "VAL:" + str(k[warning_parameter]) + ":PreVAL:" + str(pre_val) + "RATE:" + str(rate) + pre_msg + str(json.dumps(k))
										from_email = settings.EMAIL_HOST_USER
										to = "929034478@qq.com"
										try:
											send_mail(subject, text_content, from_email, [to],
													  fail_silently=False)
										except Exception as e:
											pass
								except:
									pass
							pass
						elif warning_rule.warning_type == 2:
							# 2代表差值超过某一个数值就报警
							warning_val = warning_rule.warning_val
							warning_parameter = warning_rule.parameter
							pre_val = k_pre[warning_parameter]
							if k[warning_parameter] > pre_val:
								try:
									add_val = k[warning_parameter] - pre_val
									if add_val >= warning_val:
										# 超过预设的差值，新建对应的预警实例
										nt = WarningEvent()
										nt.device_id = int(k["device_id"])
										nt.warning_time = datetime.strptime(k["time"], "%Y-%m-%d %H:%M:%S")
										nt.content = k["device_id"] + "号设备" + warning_parameter + "在" + k[
											"time"] + "增长过快，达到" + str(add_val)
										nt.save()
								except:
									pass
							pass
						else:
							# 无效编号
							pass
				except:
					# 当前设备不存在预警规则
					pass
			else:
				# 不存在次新数据，即k_pre is None
				try:
					warning_rule_list = WarningRule.objects.filter(device_id=int(k["device_id"]))
					for warning_rule in warning_rule_list:
						if warning_rule.warning_type == 0:
							warning_val = warning_rule.warning_val
							warning_parameter = warning_rule.parameter
							if k[warning_parameter] > warning_val:
								# 超过预定的数值，新建对应的预警实例
								nt = WarningEvent()
								nt.device_id = int(k["device_id"])
								nt.warning_time = datetime.strptime(k["time"], "%Y-%m-%d %H:%M:%S")
								nt.content = k["device_id"] + "号设备" + warning_parameter + "在" + k["time"] + "数值超过预期阈值"
								nt.save()
						else:
							# 由于是第一次加入数据，不存在对比
							pass
				except:
					# 当前设备不存在预警规则
					pass
			# try:
			# 	try:
			# 		# 如果以及存在最新的数据，按照规则比较这两条数据的差异
			# 		d = LatestData.objects.get(device_id=int(k["device_id"]))
			# 		if d.data_time < datetime.strptime(k["time"], "%Y-%m-%d %H:%M:%S"):
			# 			try:
			# 				warning_rule_list = WarningRule.objects.filter(device_id=int(k["device_id"]))
			# 				for warning_rule in warning_rule_list:
			# 					if warning_rule.warning_type == 0:
			# 						# 0代表超过某一个数值就报警
			# 						warning_val = warning_rule.warning_val
			# 						warning_parameter = warning_rule.parameter
			# 						if k[warning_parameter] > warning_val:
			# 							# 超过预定的数值，新建对应的预警实例
			# 							nt = WarningEvent()
			# 							nt.device_id = int(k["device_id"])
			# 							nt.warning_time = datetime.strptime(k["time"], "%Y-%m-%d %H:%M:%S")
			# 							nt.content = k["device_id"] + "号设备" + warning_parameter + "在" + k["time"] + "数值超过预期阈值"
			# 							nt.save()
			# 					elif warning_rule.warning_type == 1:
			# 						# 1代表增长率超过一定数值就报警
			# 						warning_val = warning_rule.warning_val
			# 						warning_parameter = warning_rule.parameter
			# 						pre_val = 0
			# 						if warning_parameter == "aqi":
			# 							pre_val = d.aqi
			# 						elif warning_parameter == "pm25":
			# 							pre_val = d.pm25
			# 						elif warning_parameter == "pm10":
			# 							pre_val = d.pm10
			# 						elif warning_parameter == "so2":
			# 							pre_val = d.so2
			# 						elif warning_parameter == "no2":
			# 							pre_val = d.no2
			# 						elif warning_parameter == "co":
			# 							pre_val = d.co
			# 						elif warning_parameter == "o3":
			# 							pre_val = d.o3
			# 						pre_msg = ""
			# 						pre_msg += "pre_data: aqi=" + str(d.aqi) + ",pm25=" + str(d.pm25) + ",pm10=" + str(d.pm10)\
			# 								   + ",so2=" + str(d.so2)  + ",no2=" + str(d.no2)  + ",co=" + str(d.co)  + ",o3=" + str(d.o3) + ",time=" + str(d.data_time)
			# 						if k[warning_parameter] > pre_val:
			# 							try:
			# 								rate = (k[warning_parameter] - pre_val) / pre_val
			# 								if rate >= warning_val:
			# 									# 超过预设的百分比，新建对应的预警实例
			# 									nt = WarningEvent()
			# 									nt.device_id = int(k["device_id"])
			# 									nt.warning_time = datetime.strptime(k["time"], "%Y-%m-%d %H:%M:%S")
			# 									nt.content = k["device_id"] + "号设备" + warning_parameter + "在" + k["time"] + "增长率超过预期阈值，达到" + str(rate)
			# 									nt.save()
			# 									subject = u"增长过快通知"
			# 									text_content = nt.content + "VAL:" + str(k[warning_parameter]) + ":PreVAL:" + str(pre_val) + "RATE:" + str(rate) + pre_msg + str(json.dumps(k))
			# 									from_email = settings.EMAIL_HOST_USER
			# 									to = "929034478@qq.com"
			# 									try:
			# 										send_mail(subject, text_content, from_email, [to],
			# 												  fail_silently=False)
			# 									except Exception as e:
			# 										pass
			# 							except:
			# 								pass
			# 						pass
			# 					elif warning_rule.warning_type == 2:
			# 						# 2代表差值超过某一个数值就报警
			# 						warning_val = warning_rule.warning_val
			# 						warning_parameter = warning_rule.parameter
			# 						pre_val = 0
			# 						if warning_parameter == "aqi":
			# 							pre_val = d.aqi
			# 						elif warning_parameter == "pm25":
			# 							pre_val = d.pm25
			# 						elif warning_parameter == "pm10":
			# 							pre_val = d.pm10
			# 						elif warning_parameter == "so2":
			# 							pre_val = d.so2
			# 						elif warning_parameter == "no2":
			# 							pre_val = d.no2
			# 						elif warning_parameter == "co":
			# 							pre_val = d.co
			# 						elif warning_parameter == "o3":
			# 							pre_val = d.o3
			# 						if k[warning_parameter] > pre_val:
			# 							try:
			# 								add_val = k[warning_parameter] - pre_val
			# 								if add_val >= warning_val:
			# 									# 超过预设的差值，新建对应的预警实例
			# 									nt = WarningEvent()
			# 									nt.device_id = int(k["device_id"])
			# 									nt.warning_time = datetime.strptime(k["time"], "%Y-%m-%d %H:%M:%S")
			# 									nt.content = k["device_id"] + "号设备" + warning_parameter + "在" + k[
			# 										"time"] + "增长过快，达到" + str(add_val)
			# 									nt.save()
			# 							except:
			# 								pass
			# 						pass
			# 					else:
			# 						# 无效编号
			# 						pass
			# 			except:
			# 				# 当前设备不存在预警规则
			# 				pass
			# 		# 生成完对应的规则之后，替换当前最信值
			# 		try:
			# 			d.aqi = float(k["aqi"])
			# 		except:
			# 			d.aqi = 0
			# 		try:
			# 			d.pm25 = float(k["pm25"])
			# 		except:
			# 			d.pm25 = 0
			# 		try:
			# 			d.pm10 = float(k["pm10"])
			# 		except:
			# 			d.pm10 = 0
			# 		try:
			# 			d.so2 = float(k["so2"])
			# 		except:
			# 			d.so2 = 0
			# 		try:
			# 			d.no2 = float(k["no2"])
			# 		except:
			# 			d.no2 = 0
			# 		try:
			# 			d.co = float(k["co"])
			# 		except:
			# 			d.co = 0
			# 		try:
			# 			d.o3 = float(k["o3"])
			# 		except:
			# 			d.o3 = 0
			# 		try:
			# 			d.data_time = datetime.strptime(k["time"], "%Y-%m-%d %H:%M:%S")
			# 		except:
			# 			pass
			# 		d.save()
			# 	except LatestData.DoesNotExist:
			# 		# 不存在最新的data，则把当前获取到的最新数据填充进去
			# 		d = LatestData()
			# 		d.device_id = int(k["device_id"])
			# 		try:
			# 			d.aqi = float(k["aqi"])
			# 		except:
			# 			d.aqi = 0
			# 		try:
			# 			d.pm25 = float(k["pm25"])
			# 		except:
			# 			d.pm25 = 0
			# 		try:
			# 			d.pm10 = float(k["pm10"])
			# 		except:
			# 			d.pm10 = 0
			# 		try:
			# 			d.so2 = float(k["so2"])
			# 		except:
			# 			d.so2 = 0
			# 		try:
			# 			d.no2 = float(k["no2"])
			# 		except:
			# 			d.no2 = 0
			# 		try:
			# 			d.co = float(k["co"])
			# 		except:
			# 			d.co = 0
			# 		try:
			# 			d.o3 = float(k["o3"])
			# 		except:
			# 			d.o3 = 0
			# 		try:
			# 			d.data_time = datetime.strptime(k["time"], "%Y-%m-%d %H:%M:%S")
			# 		except:
			# 			pass
			# 		d.save()
			# 		try:
			# 			warning_rule_list = WarningRule.objects.filter(device_id=int(k["device_id"]))
			# 			for warning_rule in warning_rule_list:
			# 				if warning_rule.warning_type == 0:
			# 					warning_val = warning_rule.warning_val
			# 					warning_parameter = warning_rule.parameter
			# 					if k[warning_parameter] > warning_val:
			# 						# 超过预定的数值，新建对应的预警实例
			# 						nt = WarningEvent()
			# 						nt.device_id = int(k["device_id"])
			# 						nt.warning_time = datetime.strptime(k["time"], "%Y-%m-%d %H:%M:%S")
			# 						nt.content = k["device_id"] + "号设备" + warning_parameter + "在" + k["time"] + "数值超过预期阈值"
			# 						nt.save()
			# 				else:
			# 					# 由于是第一次加入数据，不存在对比
			# 					pass
			# 		except:
			# 			# 当前设备不存在预警规则
			# 			pass
			# except Exception as e:
			# 	print(str(e))


class ReadWarningEventThread(threading.Thread):
	def __init__(self, pid, device_id_list, send_data_to_font_thread):
		threading.Thread.__init__(self)
		self.pid = pid
		self.device_id_list = device_id_list
		self.send_data_to_font_thread = send_data_to_font_thread

	def run(self):
		while True:
			# 每5分钟检查一次是否存在未读取的报警事件
			warning_data_dic = self.read_warning()
			self.send_data_to_font_thread.send_data(json.dumps(warning_data_dic))
			time.sleep(300)

	def read_warning(self):
		warning_data_dic = {}
		for device_id in self.device_id_list:
			try:
				warning_list = WarningEvent.objects.filter(device_id=device_id, read_tag=False)
				warning_data_dic[str(device_id)] = serializer(warning_list)
			except:
				pass
		return warning_data_dic


# if __name__ == '__main__':
# 	device_id_list = [1]
# 	send_data_to_font_thread = 1
# 	new_thread = CreateWarningEventThread(1, device_id_list, send_data_to_font_thread)
# 	new_thread.start()