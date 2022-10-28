import serial


def balance_serial_test(port:str, baudrate=1200, timeout=0.5):
	ser = serial.Serial(port=port, baudrate=baudrate, timeout=timeout)
	ser.write(b'PRINT\r')
	print(float(ser.readline().decode().strip().replace(' ', '')[:-1]))
	ser.write(b'TARE\r')
	# ser.readline()
	ser.write(b'PRINT\r')
	print(float(ser.readline().decode().strip().replace(' ', '')[:-1]))
	ser.close()
	# return weight, type(weight)


if __name__ == '__main__':
	balance_serial_test(port='com3', baudrate=1200)