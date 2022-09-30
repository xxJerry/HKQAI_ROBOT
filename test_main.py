import numpy as np
import socket
import time
import struct
import util
import rtde

HOST = "192.168.1.3"
PORT = 30003


def get_current_tcp():
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.connect((HOST, PORT))
    data = tcp_socket.recv(1108)
    position = struct.unpack('!6d', data[444:492])
    tcp_socket.close()
    return np.asarray(position)

def get_current_pos():  # x, y, theta
    tcp = get_current_tcp()
    rpy = util.rv2rpy(tcp[3], tcp[4], tcp[5])
    return np.asarray([tcp[0], tcp[1], rpy[-1]])

def move_to_tcp(target_tcp):
    tool_acc = 1.2  # Safe: 0.5
    tool_vel = 0.25  # Safe: 0.2
    tool_pos_tolerance = [0.001, 0.001, 0.001, 0.05, 0.05, 0.05]
    tcp_command = "movel(p[%f,%f,%f,%f,%f,%f],a=%f,v=%f,t=0,r=0)\n" % (
        target_tcp[0], target_tcp[1], target_tcp[2], target_tcp[3], target_tcp[4],
        target_tcp[5],
        tool_acc, tool_vel)
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.connect((HOST, PORT))
    tcp_socket.send(str.encode(tcp_command))  # 利用字符串的encode方法编码成bytes，默认为utf-8类型
    tcp_socket.close()
    # 确保已达到目标点，就可以紧接着发送下一条指令
    actual_pos = get_current_tcp()
    target_rpy = util.rv2rpy(target_tcp[3], target_tcp[4], target_tcp[5])
    rpy = util.rv2rpy(actual_pos[3], actual_pos[4], actual_pos[5])
    while not (all([np.abs(actual_pos[j] - target_tcp[j]) < tool_pos_tolerance[j] for j in range(3)])
               and all([np.abs(rpy[j] - target_rpy[j]) < tool_pos_tolerance[j+3] for j in range(3)])):
        actual_pos = get_current_tcp()
        rpy = util.rv2rpy(actual_pos[3], actual_pos[4], actual_pos[5])
        time.sleep(0.01)

def get_joint_torques():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    

def increase_move(delta_x, delta_y, delta_z, delta_theta):
    tcp = get_current_tcp()
    rpy = util.rv2rpy(tcp[3], tcp[4], tcp[5])
    rpy[2] = rpy[2] + delta_theta
    target_rv = util.rpy2rv(rpy)
    target_tcp = np.asarray([tcp[0] + delta_x, tcp[1] + delta_y, tcp[2] + delta_z,
                             target_rv[0], target_rv[1], target_rv[2]])
    move_to_tcp(target_tcp)

def get_digital_output():
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.connect((HOST, PORT))
    data = tcp_socket.recv(1108)
    tool = struct.unpack('!d', data[1044:1052])[0]
    tcp_socket.close()
    return tool

def get_tcp_force():
    con = rtde.RTDE(HOST, 30004)
    con.connect()
    output_names = ['actual_TCP_force']
    output_types = ['VECTOR6D']
    con.send_output_setup(output_names, output_types, frequency=125)
    con.send_start()
    state = con.receive(True)
    actual_TCP_force = struct.unpack('!6d', state)
    return actual_TCP_force

def get_joint_states():
    con = rtde.RTDE(HOST, 30004)
    con.connect()
    output_names = ['actual_q']
    output_types = ['VECTOR6D']
    con.send_output_setup(output_names, output_types, frequency=125)
    con.send_start()
    state = con.receive(True)
    actual_q = struct.unpack('!6d', state)
    return actual_q

def check_grasp():
    con = rtde.RTDE(HOST, 30004)
    con.connect()
    output_names = ['tool_analog_input0']
    output_types = ['DOUBLE']
    con.send_output_setup(output_names, output_types, frequency=125)
    con.send_start()
    state = con.receive(True)
    voltage = struct.unpack('!d', state)
    return voltage[0] > 0.3

def grasp():
    pass

def operate_gripper():
    pass

def go_home():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    home_jpose = []
    for angle in [90, -30, -120, -120, 90, 0]:
        home_jpose.append(util.degree2rad(angle))
    s.send(("movej({}, a=1, v=1)".format(home_jpose)+"\n").encode('utf8'))

# circle center [0.445, 0.736, 0.116]
# location circle radius 0.05
# hole circle radius 0.014

# (x - 0.445)**2 + (y - 0.736)**2 = 0.05**2
# x_max = 0.495, y = 0.736, z = 0.116 + 0.01 = 0.126
def get_discretized_poses():
    phi_xmax = 0
    # delta_z = 0.01
    delta_phi = 0.56
    discretized_poses = []
    for num in range(int(2*np.pi/(delta_phi/2))):
        x = 0.445 + 0.05 * np.sin(phi_xmax + num * delta_phi/2)
        y = 0.736 + 0.05 * np.cos(phi_xmax + num * delta_phi/2)
        discretized_poses.append([x,
            y,
            0.124, # z
            0.334, # rx
            3.024, # ry
            0.187]) # rz
    return discretized_poses

if __name__ == '__main__':
    wpts=[[0.379,0.375,0.229,0.334,3.024,0.187],
    [0.379,0.707,0.222,0.334,3.024,0.188],
    [0.450, 0.779, 0.123, 0.334, 3.024, 0.187]
    ]
    go_home()
    time.sleep(12)
    print([q for q in map(util.rad2degree, get_joint_states())])

    move_to_tcp(wpts[0])
    time.sleep(12)
    print([q for q in map(util.rad2degree, get_joint_states())])

    move_to_tcp(wpts[1])
    time.sleep(12)
    print([q for q in map(util.rad2degree, get_joint_states())])

    place_poses = get_discretized_poses()
    for place_pose in place_poses:
        move_to_tcp(place_pose)
        time.sleep(12)
        print([q for q in map(util.rad2degree, get_joint_states())])
        print("joint_torque:{}".format(get_joint_torques()))
        move_to_tcp(wpts[1])
        time.sleep(12)
        print([q for q in map(util.rad2degree, get_joint_states())])

    go_home()
    time.sleep(12)
    print([q for q in map(util.rad2degree, get_joint_states())])
