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

	def build_connect(self):
		self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		while True:
			try:
				self.tcp_socket.connect((self.host, self.port))
			except ConnectionError as e:
				print("Connection building failed: {}".format(e))
				_ = input("Please press any key if ready to retry\n")
			else:
				break

	def send_command(self, tcp_command: str):
		while True:
			try:
				self.tcp_socket.send(str.encode(tcp_command))
			except ConnectionResetError as e:
				print("Command sending failed: {}".format(e))
				_ = input("Please press any key if ready to retry\n")
				self.build_connect()
			else:
				break

	def recv_data(self, bufsize: int = 1024):
		while True:
			try:
				return self.tcp_socket.recv(bufsize).decode().strip()
			except ConnectionResetError as e:
				print("Data receiving failed: {}".format(e))
				_ = input("Please press any key if ready to retry\n")
				self.build_connect()

	def close_socket(self):
		self.tcp_socket.close()


def connect_test(*, host1, host2, tcp_command):
	RG2 = TcpSocket(host1)
	RG2.build_connect()
	print("Connection with RG2 built!")
	RG2.close_socket()

	DH = TcpSocket(host2)
	DH.build_connect()
	print("Connection with DH built!")
	DH.close_socket()


if __name__ == '__main__':
	connect_test(tcp_command='play\n', host1='192.168.1.3', host2='192.168.1.4')

# RG2 = TcpSocket('192.168.1.3')
# RG2.create_socket()
# RG2.close_socket()


		
