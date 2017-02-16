# coding=utf-8
import time
import random
import json


class CmdJoin:
	def __init__(self):
		self.cmdseq = ""
		self.appeui = ""
		self.appkey = ""

	'''
	    函数名称: create_cmd_join
		函数功能: 生成JOIN命令消息
		参数说明:
		返回值
	'''
	def create_cmd_join(self, data):
		random_no = int(time.time())
		json_cmd = {}
		json_cmd["CMD"] = "JOIN"
		json_cmd["CmdSeq"] = data["CmdSeq"]
		json_cmd["AppEUI"] = data["AppEUI"]
		json_cmd["AppNonce"] = random_no
		json_cmd["Challenge"] = data["Challenge"]
		msg = ""
		for c in data["AppEUI"]:
			msg += (hex(ord(c)).replace('0x',''))
		for c in str(random_no):
			msg += (hex(ord(c)).replace('0x', ''))
		msg += '0000'

		random_no = hex(int('1234', 10))
		json_cmd["Challenge"] = msg


		json_cmd = json.JSONEncoder().encode(json_cmd)
		json_len = len(json_cmd)
		cmd_str = str(json_len)
		cmd_str += "\n"
		cmd_str += json_cmd
		cmd_str += "\n"
		return cmd_str
