# -*- coding: utf-8 -*-

# 为防止程序中的意外情况导致机械臂和PC的连接中断或者程序终止，程序中规定了异常处理的方式。
# 同时，实验进行过程中可能导致程序中断的情况和相应解决方案有以下几种：
# 1. 机械臂运行过程中突然拔掉网线
# 解：重新连接网线，在确认无误后在控制台输入任意字符以接续程序。
# 2. 机械臂运行过程中按下示教器的紧急停止按钮（红色）
# 解：解锁急停按钮，并手动启动机械臂，在确认无误后在控制台输入任意字符以接续程序。
# 3. 机械臂运行过程中将机械臂的“远程模式”切换到“本地模式”
# 解：此时机械臂依然处于运行状态中，手动将“本地模式”切换回“远程模式”，在确认无误后在控制台输入任意字符以接续程序。
# 4. 机械臂运行过程中将机械臂的“远程模式”切换到“本地模式”, 且在示教器上手动暂停机械臂
# 解：此时机械臂处于暂停状态，需先手动在示教器上启动机械臂，再将“本地模式”切换回“远程模式”，在确认无误后在控制台输入任意字符以接续程序。

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
            # except ConnectionError as e:
            except Exception as e:
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


def connect_test(*, host1, host2):
    RG2 = TcpSocket(host1)
    RG2.build_connect()
    print("Connection with RG2 built!")
    RG2.close_socket()

    DH = TcpSocket(host2)
    DH.build_connect()
    print("Connection with DH built!")
    DH.close_socket()


if __name__ == '__main__':
    connect_test(host1='192.168.1.3', host2='192.168.1.4')

# RG2 = TcpSocket('192.168.1.3')
# RG2.create_socket()
# RG2.close_socket()
