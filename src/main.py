# -*- coding: utf-8 -*-

# 1. 接取指定量生成物
# 2. 放入离心机
# 3. 从离心机中取出
# 4. 将离心管放入烘干箱
# 5. 从烘干箱取出

import socket
import time

from weight import weight_tare, weight_measure, get_target_weight


def put_tube_cap_on_balance(tube_no: str):
    HOST = "192.168.1.3"
    PORT = 29999
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.connect((HOST, PORT))
    tcp_command = "load f_pre_get_result_tube{}-rg2.urp\n".format(tube_no)
    tcp_socket.send(str.encode(tcp_command))
    time.sleep(3)
    tcp_command = "play\n"
    tcp_socket.send(str.encode(tcp_command))
    tcp_socket.close()


def put_tube_on_balance(tube_no: str):
    HOST = "192.168.1.3"
    PORT = 29999
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.connect((HOST, PORT))
    tcp_command = "load f_get_result_tube{}_rg2.urp\n".format(tube_no)
    tcp_socket.send(str.encode(tcp_command))
    time.sleep(3)
    tcp_command = "play\n"
    tcp_socket.send(str.encode(tcp_command))
    tcp_socket.close()

    HOST = "192.168.1.4"
    PORT = 29999
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.connect((HOST, PORT))
    tcp_command = "load f_get_result_tube{}_dh.urp\n".format(tube_no)
    tcp_socket.send(str.encode(tcp_command))
    time.sleep(3)
    tcp_command = "play\n"
    tcp_socket.send(str.encode(tcp_command))
    tcp_socket.close()


def recap_tube(tube_no: str):
    HOST = "192.168.1.3"
    PORT = 29999
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.connect((HOST, PORT))
    tcp_command = "load f_get_result_back_tube{}_rg2.urp\n".format(tube_no)
    tcp_socket.send(str.encode(tcp_command))
    time.sleep(3)
    tcp_command = "play\n"
    tcp_socket.send(str.encode(tcp_command))
    tcp_socket.close()

    HOST = "192.168.1.4"
    PORT = 29999
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.connect((HOST, PORT))
    tcp_command = "load f_get_result_back_tube{}_dh.urp\n".format(tube_no)
    tcp_socket.send(str.encode(tcp_command))
    time.sleep(3)
    tcp_command = "play\n"
    tcp_socket.send(str.encode(tcp_command))
    tcp_socket.close()


def get_product(target_weight: float = 50):
    # TODO: pending for dev.
    for i in range(1,3):
        weight_tare()
        put_tube_cap_on_balance(str(i))
        time.sleep(3)
        tube_and_cap_weight = weight_measure()

        put_tube_on_balance(str(i))
        time.sleep(3)
        tube_weight = weight_measure()

        cap_weight = tube_and_cap_weight - tube_weight
        get_target_weight(target_weight-cap_weight)

        recap_tube(str(i))


def place_tube_in_centrifuge():
    HOST = "192.168.1.3"
    PORT = 29999
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.connect((HOST, PORT))
    tcp_command = "load f_tube_into_centri_left.urp\n"
    tcp_socket.send(str.encode(tcp_command))
    time.sleep(5)
    tcp_command = "play\n"
    tcp_socket.send(str.encode(tcp_command))
    tcp_socket.close()

    HOST = "192.168.1.4"
    PORT = 29999
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.connect((HOST, PORT))
    tcp_command = "load f_tube_into_centri_right.urp\n"
    tcp_socket.send(str.encode(tcp_command))
    time.sleep(5)
    tcp_command = "play\n"
    tcp_socket.send(str.encode(tcp_command))
    tcp_socket.close()


def pick_tube_from_centrifuge():
    HOST = "192.168.1.3"
    PORT = 29999
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.connect((HOST, PORT))
    tcp_command = "load f_tube_out_centri_left.urp\n"
    tcp_socket.send(str.encode(tcp_command))
    time.sleep(5)
    tcp_command = "play\n"
    tcp_socket.send(str.encode(tcp_command))
    tcp_socket.close()

    HOST = "192.168.1.4"
    PORT = 29999
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.connect((HOST, PORT))
    tcp_command = "load f_tube_out_centri_right.urp\n"
    tcp_socket.send(str.encode(tcp_command))
    time.sleep(5)
    tcp_command = "play\n"
    tcp_socket.send(str.encode(tcp_command))
    tcp_socket.close()
 

def place_tube_in_oven():
    HOST = "192.168.1.3"
    PORT = 29999
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.connect((HOST, PORT))
    tcp_command = "load f_tube_into_oven_left.urp\n"
    tcp_socket.send(str.encode(tcp_command))
    time.sleep(5)
    tcp_command = "play\n"
    tcp_socket.send(str.encode(tcp_command))
    tcp_socket.close()

    HOST = "192.168.1.4"
    PORT = 29999
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.connect((HOST, PORT))
    tcp_command = "load f_tube_into_oven_right.urp\n"
    tcp_socket.send(str.encode(tcp_command))
    time.sleep(5)
    tcp_command = "play\n"
    tcp_socket.send(str.encode(tcp_command))
    tcp_socket.close()


def pick_tube_from_oven():
    HOST = "192.168.1.3"
    PORT = 29999
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.connect((HOST, PORT))
    tcp_command = "load f_tube_out_oven_left.urp\n"
    tcp_socket.send(str.encode(tcp_command))
    time.sleep(5)
    tcp_command = "play\n"
    tcp_socket.send(str.encode(tcp_command))
    tcp_socket.close()

    HOST = "192.168.1.4"
    PORT = 29999
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.connect((HOST, PORT))
    tcp_command = "load f_tube_out_oven_right.urp\n"
    tcp_socket.send(str.encode(tcp_command))
    time.sleep(5)
    tcp_command = "play\n"
    tcp_socket.send(str.encode(tcp_command))
    tcp_socket.close()


def main():
    get_product()
    place_tube_in_centrifuge()
    pick_tube_from_centrifuge()
    place_tube_in_oven()
    pick_tube_from_oven()


if __name__ == "main":
    main()
