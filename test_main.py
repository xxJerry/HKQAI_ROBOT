import numpy as np
from scipy.spatial.transform import Rotation as R
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

def move_tcp_to(target_tcp):
    tool_acc = 1.2  # Safe: 0.5
    tool_vel = 0.25  # Safe: 0.2
    tool_pos_tolerance = [0.001, 0.001, 0.001, 0.05, 0.05, 0.05]
    tcp_command = "movel(p[%f,%f,%f,%f,%f,%f],a=%f,v=%f,t=0,r=0)\n" % (
        target_tcp[0], target_tcp[1], target_tcp[2], target_tcp[3], target_tcp[4],
        target_tcp[5],
        tool_acc, tool_vel)
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.connect((HOST, PORT))
    tcp_socket.send(str.encode(tcp_command))  # implement the encode method of string to encode command as bytes，defaults to utf-8.
    tcp_socket.close()
    # make sure the target pose is reached，and then the next command could be sent right after that.
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
    move_tcp_to(target_tcp)

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

def rg_control(target_width):
    # assert(target_width in [0, 28, 80])
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

def grasp():
    rg_control(33)

def release():
    rg_control(43)

def detect():
    rg_control(0)

def go_home():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    home_jpose = []
    for angle in [90, -30, -120, -120, 90, 0]:
        home_jpose.append(util.degree2rad(angle))
    s.send(("movej({}, a=1, v=1)".format(home_jpose)+"\n").encode('utf8'))
    s.close()

def get_discretized_poses(discretized_center_pose=[0.26460, 0.74696, 0.125, 0.020, 3.136, 0.349], radius=0.035,  delta_phi = 0.56):
    # circle center [0.445, 0.736, 0.116]
    # location circle radius 0.05
    # hole circle radius 0.014
    # (x - 0.445)**2 + (y - 0.736)**2 = 0.05**2
    # x_max = 0.495, y = 0.736, z = 0.116 + 0.01 = 0.126
    # delta_z = 0.01
    discretized_poses = []
    for num in range(int(np.pi/(delta_phi/2))):
        x = discretized_center_pose[0] - radius * np.sin(num * delta_phi/2)
        y = discretized_center_pose[1] + radius * np.cos(num * delta_phi/2)
        z = discretized_center_pose[2]
        rx, ry, rz = discretized_center_pose[3:6]
        Ro = np.eye(3)
        Rz = np.eye(3)
        Ro = R.from_rotvec(np.array([rx, ry, rz])).as_matrix()
        Rz = R.from_rotvec(np.array([0, 0, num * delta_phi/2])).as_matrix()
        rx, ry, rz = R.from_matrix(Rz @ Ro).as_rotvec()
        discretized_poses.append([x,
            y,
            z, # z
            rx, # rx
            ry, # ry
            rz]) # rz

    for num in range(int(np.pi/(delta_phi/2))):
        x = discretized_center_pose[0] + radius * np.sin(num * delta_phi/2)
        y = discretized_center_pose[1] + radius * np.cos( num * delta_phi/2)
        z = discretized_center_pose[2]
        rx, ry, rz = discretized_center_pose[3:6]
        Ro = np.eye(3)
        Rz = np.eye(3)
        Ro = R.from_rotvec(np.array([rx, ry, rz])).as_matrix()
        Rz = R.from_rotvec(np.array([0, 0, -num * delta_phi/2])).as_matrix()
        rx, ry, rz = R.from_matrix(Rz @ Ro).as_rotvec()
        discretized_poses.append([x,
            y,
            z, # z
            rx, # rx
            ry, # ry
            rz]) # r

    return discretized_poses

def detect_tubes():
    via_points=[[0.26464, 0.41918, 0.27296, 0.034, 3.194, -0.006],
                [0.26460, 0.74696, 0.18314, 0.033, 3.194, -0.000]]
    go_home()
    time.sleep(12)
    print("joint_states: {}".format([q for q in map(util.rad2degree, get_joint_states())]))

    move_tcp_to(via_points[0])
    time.sleep(10)
    print("joint_states: {}".format([q for q in map(util.rad2degree, get_joint_states())]))

    move_tcp_to(via_points[1])
    time.sleep(10)
    print("joint_states: {}".format([q for q in map(util.rad2degree, get_joint_states())]))

    # Loop and search about the inside of  centrifuge
    place_poses = get_discretized_poses()
    for idx, place_pose in enumerate(place_poses):
        move_tcp_to(place_pose)
        time.sleep(4)
        print("joint_states: {}".format([q for q in map(util.rad2degree, get_joint_states())]))
        tcp_force = np.array(get_tcp_force())
        print("tcp_force:************************", tcp_force)
        if tcp_force[2] >= -2:
            print("There is a tube!")
            if idx < len(place_poses)/2:
                print("The tube is at the angle of {}".format(idx * (180 * (0.28 / np.pi))))
            elif idx >= len(place_poses)/2:
                print("The tube is at the angle of {}".format(-(idx-len(place_poses)/2) * 180 * (0.28 / np.pi)))
        elif tcp_force[2] < -2:
            print("There is nothing!")
        move_tcp_to(via_points[1])
        time.sleep(4)
        print("joint_states: {}".format([q for q in map(util.rad2degree, get_joint_states())]))

    move_tcp_to(via_points[0])
    time.sleep(10)
    print("joint_states: {}".format([q for q in map(util.rad2degree, get_joint_states())]))

    go_home()
    time.sleep(12)
    print("joint_states: {}".format([q for q in map(util.rad2degree, get_joint_states())]))

def detect_holes():
    via_points=[[0.26464, 0.41918, 0.27296, 0.034, 3.194, -0.006],
                [0.26460, 0.74696, 0.18314, 0.033, 3.194, -0.000]]
    go_home()
    time.sleep(12)
    print("joint_states: {}".format([q for q in map(util.rad2degree, get_joint_states())]))

    move_tcp_to(via_points[0])
    time.sleep(10)
    print("joint_states: {}".format([q for q in map(util.rad2degree, get_joint_states())]))

    move_tcp_to(via_points[1])
    time.sleep(10)
    print("joint_states: {}".format([q for q in map(util.rad2degree, get_joint_states())]))

    # Loop and search about the inside of  centrifuge
    place_poses = get_discretized_poses([0.26460, 0.74696, 0.110, 0.0219, 3.128, 0.384], 0.044, 0.56)
    for idx, place_pose in enumerate(place_poses):
        move_tcp_to(place_pose)
        time.sleep(4)
        print("joint_states: {}".format([q for q in map(util.rad2degree, get_joint_states())]))
        tcp_force = np.array(get_tcp_force())
        print("tcp_force:************************", tcp_force)
        if tcp_force[2] < 2:
            print("There is a hole!")
            if idx < len(place_poses)/2:
                print("The tube is at the angle of {}".format(idx * (180 * (0.28 / np.pi))))
            elif idx >= len(place_poses)/2:
                print("The tube is at the angle of {}".format(-(idx-len(place_poses)/2) * 180 * (0.28 / np.pi)))
        elif tcp_force[2] >= 2:
            print("There is nothing!")
        move_tcp_to(via_points[1])
        time.sleep(4)
        print("joint_states: {}".format([q for q in map(util.rad2degree, get_joint_states())]))

    move_tcp_to(via_points[0])
    time.sleep(10)
    print("joint_states: {}".format([q for q in map(util.rad2degree, get_joint_states())]))

    go_home()
    time.sleep(12)
    print("joint_states: {}".format([q for q in map(util.rad2degree, get_joint_states())]))

def pick():
    rg_control(43)
    time.sleep(5)
    go_home()
    time.sleep(10)
    print("joint_states: {}".format([q for q in map(util.rad2degree, get_joint_states())]))


    above_pick_pose = [0.429, 0.246, 0.239, 3.099, -0.342, -0.013]
    pick_pose = [0.429, 0.246, 0.009, 3.099, -0.342, -0.013]

    move_tcp_to(above_pick_pose)
    time.sleep(10)
    print("joint_states: {}".format([q for q in map(util.rad2degree, get_joint_states())]))

    move_tcp_to(pick_pose)
    time.sleep(10)
    print("joint_states: {}".format([q for q in map(util.rad2degree, get_joint_states())]))

    rg_control(33)

    time.sleep(10)
    move_tcp_to(above_pick_pose)
    time.sleep(10)
    print("joint_states: {}".format([q for q in map(util.rad2degree, get_joint_states())]))

def place():
    middle_pose = [0.272, 0.478, 0.323, 3.099, -0.342, -0.013]
    approach_place_pose = [0.256, 0.717, 0.241, 3.818, -0.406, 0.097]
    pre_place_pose = [0.268, 0.716, 0.188, 3.818, -0.406, 0.097]
    place_pose = [0.277, 0.770, 0.122, 3.818, -0.406, 0.097]

    move_tcp_to(middle_pose)
    time.sleep(10)
    print("joint_states: {}".format([q for q in map(util.rad2degree, get_joint_states())]))

    move_tcp_to(approach_place_pose)
    time.sleep(10)
    print("joint_states: {}".format([q for q in map(util.rad2degree, get_joint_states())]))

    move_tcp_to(pre_place_pose)
    time.sleep(10)
    print("joint_states: {}".format([q for q in map(util.rad2degree, get_joint_states())]))   

    move_tcp_to(place_pose)
    time.sleep(10)
    print("joint_states: {}".format([q for q in map(util.rad2degree, get_joint_states())]))   

    rg_control(43)
    time.sleep(10)

    move_tcp_to(pre_place_pose)
    time.sleep(10)
    print("joint_states: {}".format([q for q in map(util.rad2degree, get_joint_states())]))

    move_tcp_to(approach_place_pose)
    time.sleep(10)
    print("joint_states: {}".format([q for q in map(util.rad2degree, get_joint_states())]))

    go_home()

if __name__ == '__main__':
    pick()
    time.sleep(10)
    place()

