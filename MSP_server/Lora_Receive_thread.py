#encoding=utf-8
import threading
import SocketServer
from CmdReceive import CmdReceive
import json
from setting import address
from setting import port
from setting import AppEUI
import socket
import ctypes
from app.views.utils.mySqlUtils import MySQL
import base64
import time
from datetime import datetime
# import crc16
from app.models import Project, SensorConfigParameter, SensorDatabaseConfig,Device


ll = ctypes.cdll.LoadLibrary
sensor_config = {
	'1': 'Time',
	'2': 'BatteryVol',
	'3': 'SolarEnergyVol',
	'4': 'O3Data',
	'5': 'COData',
	'6': 'SO2Data',
	'7': 'NO2Data',
	'8': 'PM25Data',
	'9': 'PM10Data',
	'10': 'TData',
	'11': 'PData',
	'12': 'HumData',
	'13': 'LuxData',
	'14': 'HData',
}

sensor_devEui_map = {
	"4A770203000002": "1",
	"4A770203000003": "1",
	"4A770203000004": "1",
	"4A770203000005": "1",
	"4A770203000006": "1",
	"4A770203000007": "1",
	"4A770203000008": "1",
	"4A770203000009": "1",
	"4A77020300000A": "1",
	"4A77020300000B": "1",
	"4A77020300000C": "1",
	"4A77020300000D": "1",
	"4A77020300000E": "1",
	"4A77020300000F": "1",
	"4A770203000010": "1",
	"4A770203000011": "1",
}
from MSP_server.TCP_Link import TCP


class ReceiveThread(threading.Thread):
	def __init__(self, pid,log_thread):
		threading.Thread.__init__(self)
		self.pid = pid
		self.log_thread = log_thread

	def run(self):
		receive_tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		host = (address, port)
		# receive_tcp_sock.settimeout(5)

		receive_tcp_sock.connect(host)

		json_cmd = {}
		json_cmd["CMD"] = "JOIN"
		json_cmd["CmdSeq"] = 123
		json_cmd["AppEUI"] = "2c26c50203000001"
		json_cmd["AppNonce"] = "123"
		json_cmd["Challenge"] = "2c26c50203000001"
		json_cmd = json.JSONEncoder().encode(json_cmd)
		json_len = len(json_cmd)
		cmd_str = str(json_len)
		cmd_str += "\n"
		cmd_str += json_cmd
		cmd_str += "\n"
		receive_tcp_sock.send(cmd_str)

		data = receive_tcp_sock.recv(1024)
		print "The Server Response: ", repr(data), "\n"
		print "we have join the msp server"
		while True:
			print("waiting data")
			try:
				receive_tcp_sock.send("ACK")
				data = receive_tcp_sock.recv(1024)
				print "The Server Response: ", repr(data), "\n"
				# res_str = str(json.loads(data))
				data = data.split('\n')[2]
				self.parase_data(data)
			except Exception as e:
				print "here"
				print(str(e))
			# res_str = str(json.loads(data))

	def parase_data(self, data):
		print "123456"
		try:
			print data
			data_json = json.loads(data)
			# data_str = str(json.loads(data))
			# data_json = eval(data_str)
			print data_json
			if int(data_json["CODE"]) == 100:
				Receive_AppEUI = data_json["AppEUI"]
				if str(AppEUI).lower() == str(Receive_AppEUI).lower():
					print "prepare to save to log"
					CmdSeq = data_json["CmdSeq"]
					print CmdSeq
					MSG = data_json["MSG"]
					print MSG
					DevEUI = data_json["DevEUI"]
					print DevEUI
					payload = data_json["payload"]

					print payload
					print self.decode_base64(payload)
					payload = self.decode_base64(payload)
					device_id = sensor_devEui_map[DevEUI.upper()]
					try:
						dev_eui = DevEUI.upper()
						device = Device.objects.get(dev_eui=dev_eui)
						device_id = device.num
					except Device.DoesNotExist:
						print("设备不存在")
						device_id = 0
						# 新建对应的设备
						project = Project.objects.get(name=u"大气六参数")
						try:
							device_list = Device.objects.filter(project_id=project.pk).order_by('-num')
							device_id = device_list[0].num + 1
						except:
							device_id = 1

						name = u"未命名设备"
						address = u"未命名设备"
						install_time = "2017-02-23"
						install_time = datetime.strptime(install_time, "%Y-%m-%d")

						device = Device()
						device.num = device_id
						device.name = name
						device.address = address
						device.install_time = install_time
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
					print device_id
					# 找到对应的设备并对设备的数据进行解析存储
					print("payload")
					print (payload)
					self.parse_save_to_db(device_id, payload)
					with open('./' + "receive.log", 'a') as destination:
						print "iiiiii"
						destination.write(time.strftime('%Y-%m-%d %H:%M:%S  ', time.localtime(time.time())) + "DevEUI: " + DevEUI + " Data: " + self.str_encode(payload) + "\n")
					print(self.log_thread)
					print(type(self.log_thread))
					try:
						self.log_thread.send_data(time.strftime('%Y-%m-%d %H:%M:%S  ', time.localtime(
							time.time())) + "DevEUI: " + DevEUI + " Data: " + self.str_encode(payload) + "\n")
					except:
						pass
				else:
					with open('./' + "receive.log", 'a') as destination:
						destination.write(time.strftime('%Y-%m-%d %H:%M:%S  ', time.localtime(time.time())) + "Wrong AppEUI" + "\n")
					try:
						self.log_thread.send_data(
							time.strftime('%Y-%m-%d %H:%M:%S  ', time.localtime(time.time())) + "Wrong AppEUI" + "\n")
					except:
						pass
			else:
				with open('./' + "receive.log", 'a') as destination:
					destination.write(time.strftime('%Y-%m-%d %H:%M:%S  ', time.localtime(time.time())) + "Wrong Code" + "\n")
		except Exception as e:
			with open('./' + "receive.log", 'a') as destination:
				destination.write(time.strftime('%Y-%m-%d %H:%M:%S  ', time.localtime(time.time())) + str(e) + "\n")
			print(str(e))

	def parse_save_to_db(self, device_id, data):
		# data = self.decode_base64(data)
		# data is the str which length is 52
		try:
			data_len = len(data)
			print(data_len)
			# array_type_in = ctypes.c_char * data_len
			# array_type_out = ctypes.c_char * data_len
			# datas_out = array_type_in()
			# datas_in = array_type_out()
			# idx = 0
			# for i in data:
			# 	datas_in[idx] = i
			# 	idx += 1
			# api = ll('./transform.so')
			# api.StringToHex(datas_in, datas_out, data_len)
			# out_str = ""
			# for t in datas_out:
			# 	out_str += str(t)
			out_str = data
			bin_str = self.str_encode(out_str)
			pre_data = bin_str[0:400]
			src_data = bin_str[400:408]
			# CRC_Tool = crc16()
			# crc_str = CRC_Tool.createarray(pre_data)
			crc_result = 0
			if crc_result == 0:
				'''转换设备ID'''
				tmp_1 = bin_str[0:8]
				tmp_2 = bin_str[8:16]
				device_id_bin = self.bin2dec(tmp_2 + tmp_1)
				'''转换配置表'''
				print bin_str[16:32]
				tmp_1 = bin_str[16:24]
				tmp_2 = bin_str[24:32]
				config = tmp_2 + tmp_1  # bin_str[24:40]
				'''反转配置表，从低位对应传感器'''
				config = config[::-1]

				'''转换时间'''
				time_str = bin_str[32:64]
				s1 = bin_str[32:40]
				s2 = bin_str[40:48]
				s3 = bin_str[48:56]
				s4 = bin_str[56:64]
				time_str = s4 + s3 + s2 + s1
				time_year = self.bin2dec((time_str[26:32]))
				time_month = self.bin2dec((time_str[22:26]))
				time_date = self.bin2dec((time_str[17:22]))
				time_hour = self.bin2dec((time_str[12:17]))
				time_min = self.bin2dec((time_str[6:12]))
				time_sec = self.bin2dec((time_str[0:6]))
				collect_time = "201" + str(time_year) + "-" + str(time_month) + "-" + str(time_date) + " " + str(
					time_hour) + ":" + str(time_min) + ":" + str(time_sec)
				print(collect_time)

				'''计算存入数据库的SQL需要的参数内容'''
				data = {}
				data[u"设备类型编号"] = 1
				data[u"设备编号"] = int(device_id)
				data[u"项目内节点编号"] = int(device_id)
				data[u"传感器配置表"] = 1
				data[u"紧缩型时间传感器_实时时间"] = collect_time
				data[u"电池电压传感器_电压"] = 1
				data[u"太阳能电压传感器_电压"] = 1
				data["O3_O3"] = "0"
				data["CO_CO"] = "0"
				data["SO2_SO2"] = "0"
				data["NO2_NO2"] = "0"
				data["PM2_5_PM2_5"] = "0"
				data["PM10_PM10"] = "0"

				sensor_database_config = {
					'1': 'Time',
					'2': u'电池电压传感器_电压',
					'3': u'太阳能电压传感器_电压',
					'4': 'O3_O3',
					'5': 'CO_CO',
					'6': 'SO2_SO2',
					'7': 'NO2_NO2',
					'8': 'PM2_5_PM2_5',
					'9': 'PM10_PM10',
					'10': 'TData',
					'11': 'PData',
					'12': 'HumData',
					'13': 'LuxData',
					'14': 'HData',
				}
				# 获取解析参数
				sensor_config_parameter = {}
				for i in range(14):
					idx = int(i) + 1
					try:
						sensor = SensorConfigParameter.objects.get(code=idx)
						sensor_config_parameter[str(idx)] = sensor.val
					except:
						sensor_config_parameter[str(idx)] = 1
						pass
				config = config[1:]
				for idx, tag in enumerate(config):
					if int(tag) == 1:
						print(sensor_config[str(idx + 2)]), " has data"
						tmp1 = bin_str[64 + int(idx) * 16:64 + int(idx + 1) * 16][0:8]
						tmp2 = bin_str[64 + int(idx) * 16:64 + int(idx + 1) * 16][8:16]
						data_bin = tmp2 + tmp1
						data_dec = self.bin2dec(data_bin) / sensor_config_parameter[str(idx + 2)]
						print(data_dec)
						try:
							data[sensor_database_config[str(idx + 2)]] = float(data_dec)
						except Exception as e:
							print(str(e))
							data[sensor_database_config[str(idx + 2)]] = float(0)
				# 需要计算插入数据库的SQL语句
				# 存入数据库
				data_t = {}
				data_t[u"设备类型编号"] = 1
				data_t[u"设备编号"] = int(device_id)
				data_t[u"项目内节点编号"] = int(device_id)
				data_t[u"传感器配置表"] = 1
				data_t[u"紧缩型时间传感器_实时时间"] = collect_time
				data_t[u"电池电压传感器_电压"] = data[u"电池电压传感器_电压"]
				data_t[u"太阳能电压传感器_电压"] = data[u"太阳能电压传感器_电压"]
				data_t["O3_O3"] = data["O3_O3"]
				data_t["CO_CO"] = data["CO_CO"]
				data_t["SO2_SO2"] = data["SO2_SO2"]
				data_t["NO2_NO2"] = data["NO2_NO2"]
				data_t["PM2_5_PM2_5"] = data["PM2_5_PM2_5"]
				data_t["PM10_PM10"] = data["PM10_PM10"]
				print(data_t)
				sql = MySQL()
				sql.connectDB("jssf")
				result = sql.insert_data(u"大气六参数", data_t)
				if result == "success":
					print("Save success")
				else:
					print("Save Failed")
				sql.close_connect()
			else:
				print("CRC 校验失败")
				return 0
		except Exception as e:
			print(str(e))
			print("1234567")

	def str_encode(self, s):
		s_str = ""
		for c in s:
			new_str = ""
			str_tmp = bin(ord(c)).replace('0b', '')
			if len(str_tmp) < 8:
				for i in range(8 - len(str_tmp)):
					new_str += "0"
				new_str += str_tmp
			else:
				new_str = str_tmp
			s_str += new_str
		return s_str

	def bin_decode(self, s):
		return ''.join([chr(i) for i in [int(b, 2) for b in s.split(' ')]])

	def bin2dec(self, string_num):
		return int(string_num, 2)

	def decode_base64(self,data):
		"""Decode base64, padding being optional.
		:param data: Base64 data as an ASCII byte string
		:returns: The decoded byte string.
		"""
		missing_padding = 4 - len(data) % 4
		if missing_padding:
			data += b'=' * missing_padding
		print data
		return base64.decodestring(data)

# new_thread = ReceiveThread(1)
# new_thread.start()





# def parse_save_to_db(self, device_id, data):
# 	data = self.decode_base64(data)
# 	# data is the str which length is 52
# 	try:
# 		data_len = len(data)
# 		array_type_in = ctypes.c_char * data_len
# 		array_type_out = ctypes.c_char * data_len
# 		datas_out = array_type_in()
# 		datas_in = array_type_out()
# 		idx = 0
# 		for i in data:
# 			datas_in[idx] = i
# 			idx += 1
# 		api = ll('./transform.so')
# 		api.StringToHex(datas_in, datas_out, data_len)
# 		out_str = ""
# 		for t in datas_out:
# 			print t
# 			out_str += str(t)
#
# 		bin_str = self.str_encode(out_str)
# 		pre_data = bin_str[0:400]
# 		src_data = bin_str[400:408]
#
# 		CRC_Tool = crc16()
# 		crc_str = CRC_Tool.createarray(pre_data)
# 		crc_result = CRC_Tool.calcrc(src_data)
#
# 		if crc_result == 0:
# 			Head = self.bin_decode(bin_str[0:8])
# 			device_id_bin = self.bin_decode(bin_str[8:24])
# 			config = bin_str[24:40]
# 			config.reverse()
# 			time_year = self.bin2dec(self.bin_decode(bin_str[40:46]))
# 			time_month = self.bin2dec(self.bin_decode(bin_str[46:50]))
# 			time_date = self.bin2dec(self.bin_decode(bin_str[50:55]))
# 			time_hour = self.bin2dec(self.bin_decode(bin_str[55:60]))
# 			time_min = self.bin2dec(self.bin_decode(bin_str[60:66]))
# 			time_sec = self.bin2dec(self.bin_decode(bin_str[66:72]))
# 			collect_time = "20" + str(time_year) + "-" + str(time_month) + "-" + str(time_date) + " " + str(
# 				time_hour) + ":" + str(time_min) + ":" + str(time_sec)
# 			# sql = MySQL()
# 			# sql.connectDB("jssf")
# 			data = {}
# 			data[u"设备类型编号"] = 1
# 			data[u"设备编号"] = int(device_id)
# 			data[u"项目内节点编号"] = int(device_id)
# 			data[u"传感器配置表"] = 1
# 			data[u"紧缩型时间传感器_实时时间"] = collect_time
# 			data[u"电池电压传感器_电压"] = 1
# 			data[u"太阳能电压传感器_电压"] = 1
# 			data["O3_O3"] = "0"
# 			data["CO_CO"] = "0"
# 			data["SO2_SO2"] = "0"
# 			data["NO2_NO2"] = "0"
# 			data["PM2_5_PM2_5"] = "0"
# 			data["PM10_PM10"] = "0"
# 			try:
# 				sensor_database_config = {}
# 				sensor_config_parameter = {}
# 				project = Project.objects.get(name=u"大气六参数")
# 				sensor_config_parameter_list = SensorConfigParameter.objects.filter(project_id=project.pk).order_by(
# 					'code')
# 				for scp in sensor_config_parameter_list:
# 					sensor_config_parameter[str(scp.code)] = scp.val
# 				sensor_database_config_list = SensorDatabaseConfig.objects.filter(project_id=project.pk).order_by(
# 					'code')
# 				for sdc in sensor_database_config_list:
# 					sensor_database_config[str(sdc.code)] = sdc.val
# 			except:
# 				sensor_database_config = {
# 					'1': 'Time',
# 					'2': u'电池电压传感器_电压',
# 					'3': u'太阳能电压传感器_电压',
# 					'4': 'O3_O3',
# 					'5': 'CO_CO',
# 					'6': 'SO2_SO2',
# 					'7': 'NO2_NO2',
# 					'8': 'PM2_5_PM2_5',
# 					'9': 'PM10_PM10',
# 					'10': 'TData',
# 					'11': 'PData',
# 					'12': 'HumData',
# 					'13': 'LuxData',
# 					'14': 'HData',
# 				}
# 				sensor_config_parameter = {
# 					'1': 1000,
# 					'2': 1000,
# 					'3': 1000,
# 					'4': 1000,
# 					'5': 1000,
# 					'6': 1000,
# 					'7': 1000,
# 					'8': 1000,
# 					'9': 1000,
# 					'10': 1000,
# 					'11': 1000,
# 					'12': 1000,
# 					'13': 1000,
# 					'14': 1000,
# 				}
# 			for idx, tag in enumerate(config):
# 				if int(tag) == 1:
# 					print(sensor_config[str(idx + 1)]), " has data"
# 					data_bin = bin_str[72 + int(idx) * 16:72 + int(idx + 1) * 16]
# 					data_dec = self.bin2dec(data_bin) / sensor_config_parameter[str(idx + 1)]
# 					try:
# 						data[sensor_database_config[str(idx + 1)]] = float(data_dec)
# 					except Exception as e:
# 						print(str(e))
# 						data[sensor_database_config[str(idx + 1)]] = float(0)
# 			# 需要计算插入数据库的SQL语句
#
# 			# 存入数据库
# 			print(data)
# 		# result = sql.insert_data(u"大气六参数", data)
# 		# if result == "success":
# 		# 	print("Save success")
# 		# else:
# 		# 	print("Save Failed")
# 		# sql.close_connect()
# 		else:
# 			print("CRC 校验失败")
# 			return 0
#
# 	except Exception as e:
# 		print(str(e))
