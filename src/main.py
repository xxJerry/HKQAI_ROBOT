# -*- coding: utf-8 -*-

# 1. 接取指定量生成物
# 2. 放入离心机
# 3. 从离心机中取出
# 4. 将离心管放入烘干箱
# 5. 从烘干箱取出

import socket
import time

from weight import weight_tare, weight_measure, get_target_weight

HOST1 = "192.168.1.3"
HOST2 = "192.168.1.4"
PORT = 29999
# PORT = 30003
TIMEOUT = 1200
time_accu = 0


def put_tube_cap_on_balance(tube_no: str):
    global time_accu
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.settimeout(TIMEOUT)
    tcp_socket.connect((HOST1, PORT))
    # time.sleep(5)

    # tcp_command = "load f_pre_get_result_tube{}_rg2.urp\n".format(tube_no)
    tcp_socket.send("load f_pre_get_result_tube{}_rg2.urp\n".format(tube_no).encode())
    time.sleep(1)
    # tcp_command = "play\n"
    tcp_socket.send("play\n".encode())
    time.sleep(1)

    p_flag = 'PLAYING'
    while p_flag != 'STOPPED':
        tcp_socket.send("programState\n".encode())
        # tcp_socket.send("running\r".encode())
        p_flag = tcp_socket.recv(64).decode().strip().split()[0]
        # p_flag = tcp_socket.recv(32).decode().strip()
        print("At time {}s, the program at RG2 is {}".format(time_accu, p_flag))
        time.sleep(1)
        time_accu += 1

    tcp_socket.close()


def put_tube_on_balance(tube_no: str):
    global time_accu
    tcp_socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket1.settimeout(TIMEOUT)
    tcp_socket1.connect((HOST1, PORT))
    tcp_command = "load f_get_result_tube{}_rg2.urp\n".format(tube_no)
    tcp_socket1.send(str.encode(tcp_command))
    time.sleep(1)
    tcp_command = "play\n"
    tcp_socket1.send(str.encode(tcp_command))

    time.sleep(1)

    tcp_socket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket2.settimeout(TIMEOUT)
    tcp_socket2.connect((HOST2, PORT))
    tcp_command = "load f_get_result_tube{}_dh.urp\n".format(tube_no)
    tcp_socket2.send(str.encode(tcp_command))
    time.sleep(1)
    tcp_command = "play\n"
    tcp_socket2.send(str.encode(tcp_command))

    p1_flag = 'PLAYING'
    p2_flag = 'PLAYING'
    while p1_flag != 'STOPPED' or p2_flag != 'STOPPED':
        tcp_socket1.send("programState\n".encode())
        p1_flag = tcp_socket1.recv(64).decode().strip().split()[0]
        print("At time {}s, the program at RG2 is {}".format(time_accu, p1_flag))
        tcp_socket2.send("programState\n".encode())
        p2_flag = tcp_socket2.recv(64).decode().strip().split()[0]
        print("At time {}s, the program at DH is {}".format(time_accu, p2_flag))
        time.sleep(1)
        time_accu += 1

    tcp_socket1.close()
    tcp_socket2.close()


def recap_tube(tube_no: str):
    global time_accu
    tcp_socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket1.settimeout(TIMEOUT)
    tcp_socket1.connect((HOST1, PORT))
    tcp_command = "load f_get_result_back_tube{}_rg2.urp\n".format(tube_no)
    tcp_socket1.send(str.encode(tcp_command))
    time.sleep(1)
    tcp_command = "play\n"
    tcp_socket1.send(str.encode(tcp_command))

    tcp_socket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket2.settimeout(TIMEOUT)
    tcp_socket2.connect((HOST2, PORT))
    tcp_command = "load f_get_result_back_tube{}_dh.urp\n".format(tube_no)
    tcp_socket2.send(str.encode(tcp_command))
    time.sleep(1)
    tcp_command = "play\n"
    tcp_socket2.send(str.encode(tcp_command))

    p1_flag = 'PLAYING'
    p2_flag = 'PLAYING'
    while p1_flag != 'STOPPED' or p2_flag != 'STOPPED':
        tcp_socket1.send("programState\n".encode())
        p1_flag = tcp_socket1.recv(64).decode().strip().split()[0]
        print("At time {}s, the program at RG2 is {}".format(time_accu, p1_flag))
        tcp_socket2.send("programState\n".encode())
        p2_flag = tcp_socket2.recv(64).decode().strip().split()[0]
        print("At time {}s, the program at DH is {}".format(time_accu, p2_flag))
        time.sleep(1)
        time_accu += 1

    tcp_socket1.close()
    tcp_socket2.close()


def get_product(target_weight: float = 50):
    for i in range(1,3):
        weight_tare()
        put_tube_cap_on_balance(str(i))
        time.sleep(3)
        tube_cap_weight = weight_measure()
        print("The weight of tube with cap is: {}".format(tube_cap_weight))

        put_tube_on_balance(str(i))
        time.sleep(3)
        tube_weight = weight_measure()
        print("The weight of tube without cap is: {}".format(tube_weight))

        cap_weight = tube_cap_weight - tube_weight
        print("The weight of cap is: {}".format(cap_weight))
        tube_sol_weight = get_target_weight(target_weight-cap_weight)
        print("The weight of tube with cap containing solution is: {}".format(tube_sol_weight+cap_weight))

        recap_tube(str(i))


def place_tube_in_centrifuge():
    global time_accu
    tcp_socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket1.settimeout(TIMEOUT)
    tcp_socket1.connect((HOST1, PORT))
    tcp_command = "load f_centrifuge_into_left.urp\n"
    tcp_socket1.send(str.encode(tcp_command))
    time.sleep(1)
    tcp_command = "play\n"
    tcp_socket1.send(str.encode(tcp_command))

    tcp_socket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket2.settimeout(TIMEOUT)
    tcp_socket2.connect((HOST2, PORT))
    tcp_command = "load f_centrifuge_right.urp\n"
    tcp_socket2.send(str.encode(tcp_command))
    time.sleep(1)
    tcp_command = "play\n"
    tcp_socket2.send(str.encode(tcp_command))

    p1_flag = 'PLAYING'
    p2_flag = 'PLAYING'
    while p1_flag != 'STOPPED' or p2_flag != 'STOPPED':
        tcp_socket1.send("programState\n".encode())
        p1_flag = tcp_socket1.recv(64).decode().strip().split()[0]
        print("At time {}s, the program at RG2 is {}".format(time_accu, p1_flag))
        tcp_socket2.send("programState\n".encode())
        p2_flag = tcp_socket2.recv(64).decode().strip().split()[0]
        print("At time {}s, the program at DH is {}".format(time_accu, p2_flag))
        time.sleep(1)
        time_accu += 1

    tcp_socket1.close()
    tcp_socket2.close()


def pick_tube_from_centrifuge():
    global time_accu
    tcp_socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket1.settimeout(TIMEOUT)
    tcp_socket1.connect((HOST1, PORT))
    tcp_command = "load f_centrifuge_out_left.urp\n"
    tcp_socket1.send(str.encode(tcp_command))
    time.sleep(1)
    tcp_command = "play\n"
    tcp_socket1.send(str.encode(tcp_command))

    tcp_socket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket2.settimeout(TIMEOUT)
    tcp_socket2.connect((HOST2, PORT))
    tcp_command = "load f_centrifuge_right.urp\n"
    tcp_socket2.send(str.encode(tcp_command))
    time.sleep(1)
    tcp_command = "play\n"
    tcp_socket2.send(str.encode(tcp_command))

    p1_flag = 'PLAYING'
    p2_flag = 'PLAYING'
    while p1_flag != 'STOPPED' or p2_flag != 'STOPPED':
        tcp_socket1.send("programState\n".encode())
        p1_flag = tcp_socket1.recv(64).decode().strip().split()[0]
        print("At time {}s, the program at RG2 is {}".format(time_accu, p1_flag))
        tcp_socket2.send("programState\n".encode())
        p2_flag = tcp_socket2.recv(64).decode().strip().split()[0]
        print("At time {}s, the program at DH is {}".format(time_accu, p2_flag))
        time.sleep(1)
        time_accu += 1

    tcp_socket1.close()
    tcp_socket2.close()
 

def place_tube_in_oven():
    global time_accu
    tcp_socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket1.settimeout(TIMEOUT)
    tcp_socket1.connect((HOST1, PORT))
    tcp_command = "load f_tube_into_oven_left.urp\n"
    tcp_socket1.send(str.encode(tcp_command))
    time.sleep(1)
    tcp_command = "play\n"
    tcp_socket1.send(str.encode(tcp_command))

    tcp_socket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket2.settimeout(TIMEOUT)
    tcp_socket2.connect((HOST2, PORT))
    tcp_command = "load f_tube_into_oven_right.urp\n"
    tcp_socket2.send(str.encode(tcp_command))
    time.sleep(1)
    tcp_command = "play\n"
    tcp_socket2.send(str.encode(tcp_command))

    p1_flag = 'PLAYING'
    p2_flag = 'PLAYING'
    while p1_flag != 'STOPPED' or p2_flag != 'STOPPED':
        tcp_socket1.send("programState\n".encode())
        p1_flag = tcp_socket1.recv(64).decode().strip().split()[0]
        print("At time {}s, the program at RG2 is {}".format(time_accu, p1_flag))
        tcp_socket2.send("programState\n".encode())
        p2_flag = tcp_socket2.recv(64).decode().strip().split()[0]
        print("At time {}s, the program at DH is {}".format(time_accu, p2_flag))
        time.sleep(1)
        time_accu += 1

    tcp_socket1.close()
    tcp_socket2.close()


def pick_tube_from_oven():
    global time_accu
    tcp_socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket1.settimeout(TIMEOUT)
    tcp_socket1.connect((HOST1, PORT))
    tcp_command = "load f_tube_out_oven_left.urp\n"
    tcp_socket1.send(str.encode(tcp_command))
    time.sleep(1)
    tcp_command = "play\n"
    tcp_socket1.send(str.encode(tcp_command))

    tcp_socket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket2.settimeout(TIMEOUT)
    tcp_socket2.connect((HOST2, PORT))
    tcp_command = "load f_tube_out_oven_right.urp\n"
    tcp_socket2.send(str.encode(tcp_command))
    time.sleep(1)
    tcp_command = "play\n"
    tcp_socket2.send(str.encode(tcp_command))

    p1_flag = 'PLAYING'
    p2_flag = 'PLAYING'
    while p1_flag != 'STOPPED' or p2_flag != 'STOPPED':
        tcp_socket1.send("programState\n".encode())
        p1_flag = tcp_socket1.recv(64).decode().strip().split()[0]
        print("At time {}s, the program at RG2 is {}".format(time_accu, p1_flag))
        tcp_socket2.send("programState\n".encode())
        p2_flag = tcp_socket2.recv(64).decode().strip().split()[0]
        print("At time {}s, the program at DH is {}".format(time_accu, p2_flag))
        time.sleep(1)
        time_accu += 1

    tcp_socket1.close()
    tcp_socket2.close()


def main():
    get_product()
    time.sleep(1)
    place_tube_in_centrifuge()
    time.sleep(1)
    pick_tube_from_centrifuge()
    time.sleep(1)
    place_tube_in_oven()
    time.sleep(1)
    pick_tube_from_oven()


# if __name__ == "__main__":
#     main()

# get_product()
# put_tube_cap_on_balance('1')
# put_tube_on_balance('1')
# recap_tube('1')
# place_tube_in_centrifuge()
# pick_tube_from_centrifuge()
# place_tube_in_oven()
# pick_tube_from_oven()
