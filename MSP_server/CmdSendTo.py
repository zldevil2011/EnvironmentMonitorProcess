# coding=utf-8
import time
import random
import json
import base64


class CmdSendTo:
	def __init__(self):
		self.cmdseq = ""
		self.appeui = ""
		self.deveui = ""
		self.cfm = ""
		self.payload = ""
		self.pydlen = ""
		self.port = ""

	'''
		    函数名称: create_cmd_sendto
			函数功能: 生成SENDTO命令消息
			参数说明:
			返回值
		'''
	def create_cmd_sendto(self, data):
		json_cmd = {}
		json_cmd["CMD"] = "SENDTO"
		json_cmd["AppEUI"] = data["AppEUI"]
		json_cmd["CmdSeq"] = data["CmdSeq"]
		json_cmd["DevEUI"] = data["DevEUI"]
		json_cmd["Confirm"] = data["Confirm"]
		json_cmd["payload"] = base64.b64encode(data["payload"])
		# json_cmd["Port"] = data["Port"]

		json_cmd = json.JSONEncoder().encode(json_cmd)
		json_len = len(json_cmd)

		cmd_str = "\n"
		cmd_str += str(json_len)
		cmd_str += "\n"
		cmd_str += json_cmd
		cmd_str += "\n"
		print cmd_str
		return cmd_str