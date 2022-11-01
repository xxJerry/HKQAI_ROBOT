# -*- coding: utf-8 -*-

import serial
import time


def weight_tare(bal_port: str = 'COM3', bal_baudrate: int = 1200):
	balance = serial.Serial(port=bal_port, baudrate=bal_baudrate)
	balance.write(b'TARE\r')
	balance.close()


def weight_measure(bal_port: str = 'COM3', bal_baudrate: int = 1200):
	balance = serial.Serial(port=bal_port, baudrate=bal_baudrate)
	balance.write(b'PRINT\r')
	weight = float(balance.readline().decode().strip().replace(' ', '')[:-1])
	balance.close()
	return weight


def get_target_weight(target: float, pump_port: str = 'COM6', \
					  pump_baudrate: int = 9600, bal_port: str = 'COM3', bal_baudrate: int = 1200):
	# 连接蠕动泵
	pump = serial.Serial(port=pump_port, baudrate=pump_baudrate)
	print("The pump is connected via port: {}".format(pump_port))

	# 连接天平
	balance = serial.Serial(port=bal_port, baudrate=bal_baudrate)
	print("The balance is connected via port: {}".format(bal_port))

	# 设置通道1的方向为顺时针
	pump.write(b'1J\r')
	# assert pump.readline().decode() == '*'

	# 设置通道1的转速为 80 rpm
	pump.write(b'1S008000\r')
	# assert pump.readline().decode() == '*'

	speed_adjust_flag = True
	start_pump_flag = True
	while True:
		balance.write(b'PRINT\r')
		mass = float(balance.readline().decode().strip().replace(' ', '')[:-1])
		mass_diff = target - mass

		if mass_diff <= 0.03:
			# 停止通道1
			pump.write(b'1I\r')
			break
		elif mass_diff <= 1:
			if speed_adjust_flag:
				# 设置通道1的转速为 10 rpm
				pump.write(b'1S001000\r')
				speed_adjust_flag = False
			if start_pump_flag:
				# 启动通道1
				pump.write(b'1H\r')
				start_pump_flag = False
		else:
			if start_pump_flag:
				# 启动通道1
				pump.write(b'1H\r')
			time.sleep(0.5)

	# 获取完全静止后的准确质量
	time.sleep(1)
	balance.write(b'PRINT\r')
	mass = float(balance.readline().decode().strip().replace(' ', '')[:-1])
	# print("The overall weight is: {:.3f}".format(mass))

	pump.close()
	balance.close()
	return mass


if __name__ == '__main__':
	print(get_target_weight(target=50))
