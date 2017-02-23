# coding=utf-8
import threading
import time
import json
# import crc16
import SocketServer
from SocketServer import StreamRequestHandler
from setting import AppEUI
import ctypes
from app.views.utils.mySqlUtils import MySQL
import base64


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
sensor_config_parameter = {
	'1': 1,
	'2': 1,
	'3': 1,
	'4': 1,
	'5': 1,
	'6': 1,
	'7': 1,
	'8': 1,
	'9': 1,
	'10': 1,
	'11': 1,
	'12': 1,
	'13': 1,
	'14': 1,
}
sensor_devEui_map = {
	"AA00000000000001": "1"
}
# 接受WSP下发的数据
class CmdReceive(StreamRequestHandler):
	def handle(self):
		addr = self.request.getpeername()
		print 'got connection from ', addr
		# self.wfile.write('thx for your connection')
		while 1:
			data_received = self.request.recv(1024)
			if not data_received:
				break
			self.parase_data(data_received)
			self.request.send(" ")

	def parase_data(self, data):
		try:
			data_str = str(json.loads(data))
			data_json = eval(data_str)
			print data_json
			if int(data_json["CODE"]) == 100:
				Receive_AppEUI = data_json["AppEUI"]
				if AppEUI == Receive_AppEUI:
					CmdSeq = data_json["CmdSeq"]
					MSG = data_json["MSG"]
					DevEUI = data_json["DevEUI"]
					payload = data_json["payload"]
					device_id = sensor_devEui_map[DevEUI]
					# 找到对应的设备并对设备的数据进行解析存储

					print (payload)
					# self.parse_save_to_db(device_id, payload)
					with open('./' + "receive.log", 'a') as destination:
						destination.write(time.strftime('%Y-%m-%d %H:%M:%S  ', time.localtime(time.time())) + "DevEUI: " + DevEUI + " Data: " + payload + "\n")
				else:
					with open('./' + "receive.log", 'a') as destination:
						destination.write(time.strftime('%Y-%m-%d %H:%M:%S  ', time.localtime(time.time())) + "Wrong AppEUI" + "\n")
			else:
				with open('./' + "receive.log", 'a') as destination:
					destination.write(time.strftime('%Y-%m-%d %H:%M:%S  ', time.localtime(time.time())) + "Wrong Code" + "\n")
		except Exception as e:
			with open('./' + "receive.log", 'a') as destination:
				destination.write(time.strftime('%Y-%m-%d %H:%M:%S  ', time.localtime(time.time())) + str(e) + "\n")
			print(str(e))

	def parse_save_to_db(self, device_id, data):
		data = self.decode_base64(data)
		# data is the str which length is 52
		try:
			data_len = len(data)
			array_type_in = ctypes.c_char * data_len
			array_type_out = ctypes.c_char * data_len
			datas_out = array_type_in()
			datas_in = array_type_out()
			idx = 0
			for i in data:
				datas_in[idx] = i
				idx += 1
			api = ll('./transform.so')
			api.arrtest(datas_in, datas_out, data_len)
			out_str = ""
			for t in datas_out:
				print t
				out_str += str(t)

			bin_str = self.str_encode(out_str)
			pre_data = bin_str[0:400]
			src_data = bin_str[400:408]

			# CRC_Tool = crc16()
			# crc_str = CRC_Tool.createarray(pre_data)
			# crc_result = CRC_Tool.calcrc(src_data)
			crc_result = 0
			if crc_result == 0:
				Head = self.bin_decode(bin_str[0:8])
				config = bin_str[8:24]
				config.reverse()
				time_year = self.bin2dec(self.bin_decode(bin_str[24:30]))
				time_month = self.bin2dec(self.bin_decode(bin_str[30:34]))
				time_date = self.bin2dec(self.bin_decode(bin_str[34:39]))
				time_hour = self.bin2dec(self.bin_decode(bin_str[39:44]))
				time_min = self.bin2dec(self.bin_decode(bin_str[44:50]))
				time_sec = self.bin2dec(self.bin_decode(bin_str[50:56]))
				collect_time = "20" + str(time_year) + "-" + str(time_month) + "-" + str(time_date) + " " + str(time_hour) + ":" + str(time_min) + ":" + str(time_sec)
				sql = MySQL()
				sql.connectDB("jssf")
				data = {}
				data[u"设备类型编号"] = 1
				data[u"设备编号"] = int(device_id)
				data[u"项目内节点编号"] = int(device_id)
				data[u"传感器配置表"] = 1
				data[u"紧缩型时间传感器_实时时间"] = collect_time
				data[u"电池电压传感器_电压"] = 1
				data[u"太阳能电压传感器_电压"] = 1
				data["O3_O3"] = "12"
				data["CO_CO"] = "13"
				data["SO2_SO2"] = "14"
				data["NO2_NO2"] = "15"
				data["PM2_5_PM2_5"] = "16"
				data["PM10_PM10"] = "17"
				for idx, tag in enumerate(config):
					if int(tag) == 1:
						print(sensor_config[str(idx+1)]), " has data"
						data_bin = bin_str[56 + int(idx) * 16:56 + int(idx + 1) * 16]
						data_dec = self.bin2dec(data_bin) / sensor_config_parameter[str(idx+1)]
						try:
							data[sensor_database_config[str(idx+1)]] = float(data_dec)
						except Exception as e:
							print(str(e))
							data[sensor_database_config[str(idx + 1)]] = float(0)
				# 需要计算插入数据库的SQL语句

				# 存入数据库
				print(data)
				result = sql.insert_data(u"大气六参数", data)
				if result == "success":
					print("Save success")
				else:
					print("Save Failed")
				sql.close_connect()
			else:
				return 0

		except Exception as e:
			print(str(e))

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


# data = "3031323334"
# array_type = ctypes.c_char * 10
# array_type_ret = ctypes.c_char * 5
# datas_ret = array_type_ret()
# datas = array_type()
# idx = 0
#
# for i in data:
# 	datas[idx] = i
# 	idx += 1
#
#
# api = ll('./transform.so')
# api.HexToString(datas, datas_ret, 10)
# for t in datas_ret:
# 	print t


# my_server = SocketServer.ThreadingTCPServer(("139.129.25.49", 21568), CmdReceive)
# my_server.serve_forever()
