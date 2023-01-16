# -*- coding: utf-8 -*-

# 实验整体操作流程：
# 1. PC启动蠕动泵，将反应溶液注入反应容器内
# 2. 机械臂启动加热装置（按开关）
# 3. PC启动搅拌器，反应进行预定时长
# 4. PC停止搅拌器，并控制蠕动泵和电子天平配合机械臂接取指定量生成物（2管）
# 5. 机械臂将2管离心管放入离心机
# 6. 机械臂从离心机中取出2管离心管
# 7. 机械臂倒掉2管离心管内的上清液，且无需盖回盖子
# 8. 机械臂将2管离心管放入烘干箱
# 9. 机械臂从烘干箱中取出2管离心管，实验完成

import time

from weight import weight_tare, weight_measure, get_target_weight
from tcp_socket import TcpSocket, connect_test

HOST1 = "192.168.1.3"
HOST2 = "192.168.1.4"
PORT = 29999
PLAY_COMMAND = 'play\n'
PAUSE_COMMAND = 'pause\n'
STOP_COMMAND = 'stop\n'
PROGRAM_STATE_COMMAND = "programState\n"


time_accu = 0


def socket_command(*, RG2_command: str = None, DH_command: str = None):
    global time_accu

    if RG2_command is not None:
        tcp_socket1 = TcpSocket(HOST1)
        tcp_socket1.build_connect()
        tcp_socket1.send_command(RG2_command)
        print(tcp_socket1.recv_data())
        time.sleep(0.1)
        tcp_socket1.send_command(PLAY_COMMAND)
        print(tcp_socket1.recv_data())

        # time.sleep(1)

    if DH_command is not None:
        tcp_socket2 = TcpSocket(HOST2)
        tcp_socket2.build_connect()
        tcp_socket2.send_command(DH_command)
        print(tcp_socket2.recv_data())
        time.sleep(0.1)
        tcp_socket2.send_command(PLAY_COMMAND)
        print(tcp_socket2.recv_data())

    p1_flag = 'PLAYING' if RG2_command else 'STOPPED'
    p2_flag = 'PLAYING' if DH_command else 'STOPPED'

    while p1_flag != 'STOPPED' or p2_flag != 'STOPPED':
        if RG2_command is not None:
            if p2_flag == 'PAUSED' and p1_flag == 'PLAYING':
                tcp_socket1.send_command(PAUSE_COMMAND)
                # time.sleep(0.1)
                # print("Adjusting: RG2 {}".format(tcp_socket1.recv_data()))
                _ = input("Please press any key once ready for continuing\n")
                tcp_socket1.send_command(PLAY_COMMAND)
                # time.sleep(0.1)
                # print("Adjusting: RG2 {}".format(tcp_socket1.recv_data()))
                tcp_socket2.send_command(PLAY_COMMAND)
                # time.sleep(0.1)
                # print("Adjusting: DH {}".format(tcp_socket2.recv_data()))
            else:
                tcp_socket1.send_command(PROGRAM_STATE_COMMAND)
                time.sleep(0.5)
                time_accu += 0.5
                p1_flag = tcp_socket1.recv_data().split()[0]
                print("At time {}s, the program at RG2 is {}".format(time_accu, p1_flag))
        else:
            pass

        if DH_command is not None:
            if p1_flag == 'PAUSED' and p2_flag == 'PLAYING':
                tcp_socket2.send_command(PAUSE_COMMAND)
                # time.sleep(0.1)
                # print("Adjusting: DH {}".format(tcp_socket2.recv_data()))
                _ = input("Please press any key once ready for continuing\n")
                tcp_socket1.send_command(PLAY_COMMAND)
                # time.sleep(0.1)
                # print("Adjusting: RG2 {}".format(tcp_socket1.recv_data()))
                tcp_socket2.send_command(PLAY_COMMAND)
                # time.sleep(0.1)
                # print("Adjusting: DH {}".format(tcp_socket2.recv_data()))
            else:
                tcp_socket2.send_command(PROGRAM_STATE_COMMAND)
                time.sleep(0.5)
                time_accu += 0.5
                p2_flag = tcp_socket2.recv_data().split()[0]
                print("At time {}s, the program at DH is {}".format(time_accu, p2_flag))
        else:
            pass 

        # time.sleep(1)
        # time_accu += 1

    if RG2_command is not None:
        tcp_socket1.close_socket()

    if DH_command is not None:
        tcp_socket2.close_socket()


def put_tube_cap_on_balance(tube_no: int):
    socket_command(RG2_command="load f_pre_get_result_tube{}_rg2.urp\n".format(tube_no))


def put_tube_on_balance(tube_no: int):
    socket_command(RG2_command="load f_get_result_tube{}_rg2.urp\n".format(tube_no),
                   DH_command="load f_get_result_tube{}_dh.urp\n".format(tube_no))


def recap_tube(tube_no: int):
    socket_command(RG2_command="load f_get_result_back_tube{}_rg2.urp\n".format(tube_no),
                   DH_command="load f_get_result_back_tube{}_dh.urp\n".format(tube_no))


def get_product(target_weight: float = 50):
    for i in range(1, 3):
        weight_tare()
        put_tube_cap_on_balance(i)
        time.sleep(3)
        tube_cap_weight = weight_measure()
        print("The weight of tube with cap is: {}".format(tube_cap_weight))

        put_tube_on_balance(i)
        time.sleep(3)
        tube_weight = weight_measure()
        print("The weight of tube without cap is: {}".format(tube_weight))

        cap_weight = tube_cap_weight - tube_weight
        print("The weight of cap is: {}".format(cap_weight))
        tube_sol_weight = get_target_weight(target_weight-cap_weight)
        print("The weight of tube with cap containing solution is: {}"
              .format(tube_sol_weight+cap_weight))

        recap_tube(i)


def place_tube_in_centrifuge():
    socket_command(RG2_command="load f_centrifuge_into_left.urp\n",
                   DH_command="load f_centrifuge_right.urp\n")


def pick_tube_from_centrifuge():
    socket_command(RG2_command="load f_centrifuge_out_left.urp\n",
                   DH_command="load f_centrifuge_right.urp\n")


def pour_liquid():
    for i in range(1, 3):
        socket_command(RG2_command="load f_remove_cap_tube{}_rg2.urp\n".format(i),
                       DH_command="load f_remove_cap_tube{}_dh.urp\n".format(i))


def place_tube_in_oven():
    socket_command(RG2_command="load f_tube_into_oven_left.urp\n",
                   DH_command="load f_tube_into_oven_right.urp\n")


def pick_tube_from_oven():
    socket_command(RG2_command="load f_tube_out_oven_left.urp\n",
                   DH_command="load f_tube_out_oven_right.urp\n")


def main():
    get_product()
    time.sleep(1)
    place_tube_in_centrifuge()
    time.sleep(1)
    pick_tube_from_centrifuge()
    time.sleep(1)
    pour_liquid()
    time.sleep(1)
    place_tube_in_oven()
    time.sleep(1)
    pick_tube_from_oven()


# if __name__ == "__main__":
#     main()


# get_product()
# put_tube_cap_on_balance(1)
# put_tube_on_balance(1)
# recap_tube(1)
# place_tube_in_centrifuge()
# pick_tube_from_centrifuge()
connect_test(host1=HOST1, host2=HOST2)
place_tube_in_oven()
# pick_tube_from_oven()
