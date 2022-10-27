import serial


def balance_serial_test(port:str, baudrate=1200, timeout=0.5):
	ser = serial.Serial(port=port, baudrate=baudrate, timeout=timeout)
	ser.write(b'PRINT\r')
	weight = float(ser.readline().decode().strip()[:-1])
	ser.close()
	return weight, type(weight)


if __name__ == '__main__':
	print(balance_serial_test(port='com3', baudrate=1200))