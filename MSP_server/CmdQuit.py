# coding=utf-8
import time
import random
import json

class CmdQuit:
	def __init__(self):
		self.cmdseq = ""
		self.appeui = ""

	'''
	    函数名称: create_cmd_quit
		函数功能: 生成QUIT命令消息
		参数说明:
		返回值
	'''
	def create_cmd_quit(self, data):
		json_cmd = {}
		json_cmd["CMD"] = "QUIT"
		json_cmd["CmdSeq"] = data["CmdSeq"]
		json_cmd["AppEUI"] = data["AppEUI"]

		json_cmd = json.JSONEncoder().encode(json_cmd)
		json_len = len(json_cmd)

		cmd_str = str(json_len)
		cmd_str += "\n"
		cmd_str += json_cmd
		cmd_str += "\n"
		return cmd_str
