import socket
import time

class TcpSocket():
	def __init__(self, host_name, port: int = 29999):
		self.tcp_socket = None
		self.host_name = host_name
		self.port = port

	# Decorator used to handle errors.
	def error_handler(with_return_value: bool):
		def double_wrapper(func):
			@wraps(func)
			def wrapper(*args, **kwargs):
				# 'with_return_value' indicates whether the decorated function has return value.
				if with_return_value:
					while True:
						try:
							return func(self, *args, **kwargs)
						except Exception as e:
							print(e)
							_ = input("Please check the issue, and please press any key once fixed")
							continue
						# else:
						# 	print("Function {} was performed successfully!".format(func.__name__))
						# 	break
				else:
					while True:
						try:
							func(*args, **kwargs)
						except Exception as e:
							print(e)
							_ = input("Please check the issue, and please press any key once fixed")
							continue
						else:
							print("Function {} was performed successfully!".format(func.__name__))
							break
			return wrapper
		return double_wrapper


	@error_handler(True)
	def build_connect(self, robot: str):
		self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		
