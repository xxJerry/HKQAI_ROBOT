import time
import socket


def rg_control(target_width):
    assert(target_width in [0, 28, 80])
    HOST = "192.168.1.3"
    PORT = 29999
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.connect((HOST, PORT))
    tcp_command = "load rg_width{}.urp\n".format(target_width)
    tcp_socket.send(str.encode(tcp_command))
    time.sleep(3)
    tcp_command = "play\n"
    tcp_socket.send(str.encode(tcp_command))
    tcp_socket.close()

if __name__ == '__main__':
    rg_control(0)
    rg_control(80)
