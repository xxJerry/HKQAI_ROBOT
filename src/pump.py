# 本程序作蠕动泵使用参考

import serial
import time


def reglo_icc_serial_test(dev: str, baudrate=9600, timeout=0.5):
	# Create a connect
	ser = serial.Serial(port=dev, baudrate=baudrate, timeout=timeout)
	print(ser.name)
	print(ser.port)

	# Set the rotation direction of channel 2 to clockwise
	ser.write(b'2J\r')
	print(ser.read(10).decode())

	# Start channel 2 to pump and display return value
	ser.write(b'2H\r')
	print(ser.read(10).decode().strip())
	time.sleep(1.5)

	# Stop channel 2 and display return value
	ser.write(b'2I\r')
	print(ser.read(10).decode())
	time.sleep(1)

	# Acquire the rotation direction of channel 2
	ser.write(b'2xD\r')
	print(ser.read(10).decode().strip())

	# Set the rotation direction of channel 2 to counter-clockwise
	ser.write(b'2K\r')
	print(ser.read(10).decode())

	# Start channel 2 to pump and display return value
	ser.write(b'2H\r')
	print(ser.read(10).decode().strip())
	time.sleep(1.5)

	# Stop channel 2 and display return value
	ser.write(b'2I\r')
	print(ser.read(10).decode())
	time.sleep(1)

	# Adjust the speed of channel 3 to 10 rpm
	ser.write(b'3S000500\r')
	print(ser.read(10).decode().strip())

	# Start channel 3 to pump and display return value
	ser.write(b'3H\r')
	print(ser.read(10).decode())
	time.sleep(1.5)

	# Stop channel 3 and display return value
	ser.write(b'3I\r')
	print(ser.read(10).decode())
	time.sleep(1)

	# Acquire the speed of channel 3 in RPM
	ser.write(b'3S\r')
	print(ser.read(10).decode().strip())

	# Adjust the speed of channel 3 to 30 rpm
	ser.write(b'3S003000\r')
	print(ser.read(10).decode().strip())

	# Start channel 3 to pump and display return value
	ser.write(b'3H\r')
	print(ser.read(10).decode())
	time.sleep(1.5)

	# Stop channel 3 and display return value
	ser.write(b'3I\r')
	print(ser.read(10).decode())
	time.sleep(1)

	# Close the connect
	ser.close()


if __name__ == "__main__":
	reglo_icc_serial_test(dev='COM8', baudrate=9600, timeout=0.5)