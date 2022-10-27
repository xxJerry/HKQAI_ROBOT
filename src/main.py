# 1. （waitlist）接取生成物 
# 2.  (Done）称重, arg: 多重
# 3. 放入离心机
# 4. 从离心机中取出
# 5. 将离心管放入烘干箱
# 6. 从烘干箱取出
import socket

def get_product():
    # TODO: pending for dev.
    return None

def get_target_weight():
    # TODO: pending for dev
    return None

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
    get_target_weight()
    place_tube_in_centrifuge()
    pick_tube_from_centrifuge()
    place_tube_in_oven()
    pick_tube_from_oven()

if __name__ == "main":
    main()
