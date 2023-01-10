# -*- coding: utf-8 -*-


import socket
import time


HOST1 = '192.168.1.3'
HOST2 = '192.168.1.4'
PORT = 29999


class TcpSocket:
	def __init__(self, host: str, port: int = PORT):
		self.tcp_socket = None
		self.host = host
		self.port = port

	# Decorator used to handle errors.
	def error_handler(self, with_return_value: bool):
		def double_wrapper(func):
			def wrapper(*args, **kwargs):
				# 'with_return_value' indicates whether the decorated function has return value.
				while True:
					try:
						if with_return_value:
							return func(self, *args, **kwargs)
						else:
							func(*args, **kwargs)
							print("Function {} was performed successfully!".format(func.__name__))
					except Exception as e:
						print(e)
						num = -1
						while num != 1 and num != 2:
							num = input("Please check the issue, and input the option:\n \
								1: Issue solved, continue the process. \n \
								2: Further command needed. \n")
							if num == 1:
								print("You claimed the issue is solved, PC will try again now")
								break
							elif num == 2:
								next_command = input("You asked to send further command, please input it now") + '\n'
								return next_command
							else:
								print("Wrong input! Please input correct number!")
								continue
					else:
						break
			return wrapper
		return double_wrapper

	@error_handler(False)
	def create_socket(self):
		self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	@error_handler(False)
	def build_connect(self):
		self.tcp_socket.connect((self.host, self.port))

	@error_handler(False)
	def send_command(self, tcp_command: str):
		self.tcp_socket.send(str.encode(tcp_command))

	@error_handler(True)
	def recv_data(self, bufsize : int = 1024):
		data = self.tcp_socket.recv(bufsize=bufsize).decode().strip()
		return data

	@error_handler(False)
	def close_socket(self):
		self.tcp_socket.close()


def connect_test(*, host1, host2, tcp_command):
	RG2 = TcpSocket(host1)
	RG2.create_socket()
	# RG2.build_connect()
	RG2.close_socket()

	DH = TcpSocket(host2)
	DH.create_socket()
	# DH.build_connect()
	DH.close_socket()


# if __name__ == '__main__':
# 	connect_test(tcp_command='play\n', host1='192.168.1.3', host2='192.168.1.4')

# RG2 = TcpSocket('192.168.1.3')
# RG2.create_socket()
# RG2.close_socket()


		
