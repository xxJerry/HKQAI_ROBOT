# -*- coding: utf-8 -*-

import serial
import time


def get_target_weight(target: float, pump_port: str, pump_baudrate: int, \
	bal_port: str, bal_baudrate: int):
	pump = serial.Serial(port=pump_port, baudrate=pump_baudrate)
	print("The pump is connected via port: {}".format(pump_port))

	balance = serial.Serial(port=bal_port, baudrate=bal_baudrate)
	print("The balance is connected via port: {}".format(bal_port))

	# 设置通道1的方向为顺时针
	pump.write(b'1J\r')
	# assert pump.read(10).decode() == '*'

	# 设置通道1的转速为30 rpm
	pump.write(b'1S003000\r')
	# assert pump.read(10).decode() == '*'

	# 启动通道1
	pump.write(b'1H\r')

	speed_adjust_flag = True
	while True:
		balance.write(b'PRINT\r')
		mass = float(balance.read(10)[:-1])
		mass_diff = target - mass

		if mass_diff <= 0.1:
			pump.write(b'1I\r')
			break 
		elif mass_diff <= mass * 0.1 and speed_adjust_flag:
			pump.write(b'1S000500\r')
			speed_adjust_flag = False
		else:
			pass
	pump.close()
	balance.close()