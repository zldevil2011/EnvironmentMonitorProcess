from MSP_server.Lora_Receive_thread import ReceiveThread
from TCP_Link import TCP
from CmdJoin import CmdJoin
from CmdSendTo import CmdSendTo
from CmdQuit import CmdQuit
from setting import address
from setting import port
from setting import AppEUI
from setting import DevEui_list
import setting as sys_setting
import json
import time


class MSP:
	def __init__(self):
		CmdSeq = int(time.time())
		if CmdSeq % 2 == 0:
			CmdSeq += 1
		self.CmdSeq = CmdSeq
		self.HOST = address  # The remote host
		self.PORT = port  # The same port as used by the server
		self.AppEUI = AppEUI
		# self.tcp = ""
		# self.sock = ""

	def get_tcp_sock(self):
		self.tcp = TCP()
		self.sock = self.tcp.open_tcp_sock(self.HOST, self.PORT)
		if self.sock == -1:
			print("open_tcp_link_failed\n")
		else:
			print("open_tcp_link_success!\n")

	def join_server(self):
		cmd_join = CmdJoin()
		json_cmd = {}
		json_cmd["CmdSeq"] = self.CmdSeq + 2
		self.CmdSeq += 2
		json_cmd["AppEUI"] = self.AppEUI

		json_cmd["Challenge"] = "ABCDEF1234567890ABCDEF1234567890"
		client_msg = cmd_join.create_cmd_join(json_cmd)
		try:
			code = self.tcp.tcp_send_data(self.sock, client_msg)
			if int(code) == 200:
				print("Login Success\n")
				return 1
			else:
				return 0
				self.re_join_server(json_cmd["AppEUI"])

		except Exception as e:
			print("Send Join Information Failed\n")
			return 0
			self.re_join_server(json_cmd["AppEUI"])

	def re_join_server(self, AppEui):
		print("Login Failed\n")
		print("Your Login Information:\n")
		print("Address", address)
		print("Port", port)
		print("AppEUI", AppEui)
		print("Do you want to try again?(y/n)")
		choice = raw_input()
		if choice == "y":
			self.join_server()
		else:
			pass

	def sendto_server(self, DevEUI, payload, Confirm):
		cmd_sendto = CmdSendTo()
		json_cmd = {}
		json_cmd["CMD"] = "SENDTO"
		json_cmd["AppEUI"] = self.AppEUI
		json_cmd["CmdSeq"] = self.CmdSeq + 2
		self.CmdSeq += 2
		json_cmd["DevEUI"] = DevEUI
		json_cmd["Confirm"] = Confirm
		json_cmd["payload"] = payload
		# json_cmd["Port"] = 21
		# print json_cmd
		client_msg = cmd_sendto.create_cmd_sendto(json_cmd)
		try:
			code = self.tcp.tcp_send_data(self.sock, client_msg)
			if int(code) == 200:
				print("SendTo Success\n")
				return 1
			else:
				print("SendTo Failed\n")
				return 0
		except Exception as e:
			print(str(e))
			print("SendTo Information Failed\n")
			return 0

	# def sendto_cs(self):
	# 	json_cmd = {}
	# 	json_cmd["CODE"] = 100
	# 	json_cmd["AppEUI"] = "AA555A0000000000"
	# 	json_cmd["CmdSeq"] = 4
	# 	json_cmd["MSG"] = "UPLOAD"
	# 	json_cmd["DevEUI"] = "AA00000000000001"
	# 	json_cmd["payload"] = "0F0A0B0304050203060B030A030C0E0F"
	# 	json_cmd["Port"] = 21
	#
	# 	json_cmd = json.JSONEncoder().encode(json_cmd)
	# 	client_msg = json_cmd
	# 	print client_msg
	# 	try:
	# 		print("prepare to send to cs")
	# 		code = self.tcp.tcp_send_data(self.sock, client_msg)
	# 		print("SendTo To CS  Success\n")
	# 	except Exception as e:
	# 		print("SendTo to CS Information Failed\n")

	def receive_from_msp(self):
		try:
			new_thread = ReceiveThread(1, 2)
			new_thread.start()
		except Exception as e:
			print(str(e))
	def quit_server(self):
		cmd_quit = CmdQuit()
		json_cmd = {}
		json_cmd["CMD"] = "QUIT"
		json_cmd["AppEUI"] = self.AppEUI
		json_cmd["CmdSeq"] = self.CmdSeq + 2
		self.CmdSeq += 2
		client_msg = cmd_quit.create_cmd_quit(json_cmd)
		try:
			code = self.tcp.tcp_send_data(self.sock, client_msg)
			if int(code) == 200:
				print("Quit Success\n")
				return 1
			else:
				print("Quit Failed\n")
				return 0
		except Exception as e:
			print("Quit Information Failed\n")
			return 0


if __name__ == "__main__":

	msp = MSP()
	try:
		msp.get_tcp_sock()
	except Exception as e:
		print(str(e))
		print("open tcp failed")
	while True:
		print("The Menu:")
		print("J:JOIN")
		print("S:SENDTO")
		print("Q:QUIT")
		print("SC:QUIT")
		print("Please select the Operation: J  S  Q SC:")
		operation = raw_input()

		if operation == "J":
			res = msp.join_server()
		elif operation == "S":
			res = msp.sendto_server("004A770203000002","update paramter", True)
		elif operation == "Q":
			res = msp.quit_server()
			break
		elif operation == "SC":
			msp.receive_from_msp()

	try:
		msp.tcp.tcp_close_sock(msp.sock)
	except Exception as e:
		print("close Tcp Failed")