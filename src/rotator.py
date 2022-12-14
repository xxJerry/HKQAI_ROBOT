# -*- coding: utf-8 -*-

import time
import serial
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu

# 注意：由于厂家硬件连接错误，导致此型号搅拌头只能使用启动(start_rotator)与停止(stop_rotator)两项功能
# cst.READ_HOLDING_REGISTERS 代表指令0x03 （读）
# cst.WRITE_MULTIPLE_REGISTERS 代表指令0x10 (写)
# 1个寄存器占有两个字节


class Rotator:
	def __init__(self, port: str = 'com10', baudrate: int = 9600):
		self.master = modbus_rtu.RtuMaster(serial.Serial(port=port, \
			baudrate=baudrate,  parity=serial.PARITY_EVEN))
		self.master.set_timeout(5.0)

	# 获取实际的运行时间（单位：小时 或 分钟）
	def get_actual_runtime(self, unit_scale: str):
		# 单位：小时
		if unit_scale == "hour":
			read_out = self.master.execute(3, cst.READ_HOLDING_REGISTERS, starting_address=0x0A, quantity_of_x=1)
			print("实际的运行时间为： {} {}s".format(read_out, unit_scale))
		# 单位：分钟
		else:
			read_out = self.master.execute(3, cst.READ_HOLDING_REGISTERS, starting_address=0x0B, quantity_of_x=1)
			print("实际的运行时间为： {} {}s".format(read_out, unit_scale))
		return read_out

	# 获取设定的运行时间（单位：小时 或 分钟）
	def get_set_runtime(self, unit_scale: str):
		# 单位：小时
		if unit_scale == "hour":
			read_out = self.master.execute(3, cst.READ_HOLDING_REGISTERS, starting_address=0x22, quantity_of_x=1)
			print("设定的运行时间为： {} {}s".format(read_out, unit_scale))
		# 单位：分钟
		else:
			read_out = self.master.execute(3, cst.READ_HOLDING_REGISTERS, starting_address=0x23, quantity_of_x=1)
			print("设定的运行时间为： {} {}s".format(read_out, unit_scale))
		return read_out

	# 获取当前实际的转速（单位：rpm）
	def get_actual_speed(self):
		read_out = self.master.execute(3, cst.READ_HOLDING_REGISTERS, starting_address=0x16, quantity_of_x=1)
		print("实际的转速为： {} rpm".format(read_out))
		return read_out

	# 获取当前设定的转速（单位：rpm）
	def get_set_speed(self):
		read_out = self.master.execute(3, cst.READ_HOLDING_REGISTERS, starting_address=0x17, quantity_of_x=1)
		print("设定的转速为： {} rpm".format(read_out))
		return read_out

	# 启动搅拌器
	def start_rotator(self):
		self.master.execute(3, cst.WRITE_MULTIPLE_REGISTERS, starting_address=0x1000, output_value=[0x0c])
		# read_out = self.master.execute(3, cst.READ_HOLDING_REGISTERS, 0x1000, 1)[0]
		# if read_out != 0x0c:
		# 	raise Exception("Fail to start the rotator!", read_out)
		# else:
		# 	print("Rotator successfully stopped! {}".format(hex(read_out)))

	def stop_rotator(self):
		self.master.execute(3, cst.WRITE_MULTIPLE_REGISTERS, starting_address=0x1000, output_value=[0x03])
		# read_out = self.master.execute(3, cst.READ_HOLDING_REGISTERS, 0x1000, 1)[0]
		# if read_out != 0x03:
		# 	raise Exception("Fail to stop the rotator!", read_out)
		# else:
		# 	print("Rotator successfully stopped! {}".format(hex(read_out)))

	def set_speed(self, speed: int):
		if speed > 3000 or speed < 0:
			raise Exception("Wrong speed value! Please set the value in range [0, 3000]")
		self.master.execute(3, cst.WRITE_MULTIPLE_REGISTERS, starting_address=0x400, output_value=[speed])
		read_out = self.master.execute(3, cst.READ_HOLDING_REGISTERS, 0x400, 1)[0]
		if read_out != speed:
			raise Exception("Fail to set the speed correctly!", hex(read_out))
		else:
			print("Successfully set the speed! {}".format(hex(read_out)))

	def set_runtime(self, runtime: int):
		if runtime > 9000 or runtime < 0:
			raise Exception("Wrong runtime! Please set the value in range [0, 9999]")
		self.master.execute(3, cst.WRITE_MULTIPLE_REGISTERS, starting_address=0x401, output_value=[runtime])
		read_out = self.master.execute(3, cst.READ_HOLDING_REGISTERS, 0x401, 1)[0]
		if read_out != runtime:
			raise Exception("Fail to set the runtime correctly!", hex(read_out))
		else:
			print("Successfully set the runtime! {}".format(hex(read_out)))


if __name__ == '__main__':
	rotator = Rotator(port='com8')
	rotator.start_rotator()
	print("Rotator started!")
	time.sleep(5)
	rotator.stop_rotator()
	print("Rotator stopped!")
