# coding=utf-8
import socket
import json


class TCP:
	def __init__(self):
		self.type = "TCP"

	def get_tcp_host(self, HOST, PORT):
		try:
			host = (HOST, PORT)
			return host
		except Exception as e:
			return None

	def open_tcp_sock(self, HOST, PORT):
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		except Exception as e:
			print("Open socket failed!\n")
			return -1

		host = self.get_tcp_host(HOST, PORT)

		if host is None:
			print("Get host failed!\n")
			return -1
		# s.settimeout(5)
		try:
			s.connect(host)
		except Exception as e:
			print(str(e))
			print("Connect to MSP server failed!\n")
			return -1

		print("Connect to MSP server SUCCESS!\n")
		return s

	def tcp_send_data(self, sock, client_msg):
		sock.send(client_msg)
		ret_code = 400
		try:
			data = sock.recv(1024)
			print "The Server Response: ", repr(data), "\n"
			res_str = str(json.loads(data))
			response_json = eval(res_str)
			ret_code = response_json["CODE"]
		except Exception as e:
			ret_code = 400
			print(str(e))
		return ret_code

	def tcp_close_sock(self, s):
		s.close()