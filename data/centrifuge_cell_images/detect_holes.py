import pyrealsense2 as rs
import cv2
import numpy as np
import time

def empty(a):
    pass

def draw_direction(img, lx, ly, nx, ny):
    dx = nx - lx
    dy = ny - ly
    if abs(dx) < 4 and abs(dy) < 4:
        dx = 0
        dy = 0
    else:
        r = (dx**2 + dy**2)**0.5
        dx = int(dx/r*40)
        dy = int(dy/r*40)
        # print(dx, dy)
    cv2.arrowedLine(img, (60, 100), (60+dx, 100+dy), (0, 255, 0), 2)
    # print(nx-lx, ny-ly)   # 噪声一般为+-1
    # cv2.arrowedLine(img, (150, 150), (150+(nx-lx), 150+(ny-ly)), (0, 0, 255), 2, 0, 0, 0.2)

def Hough_circle(imgGray, canvas):
    # 基于霍夫圆检测找圆，包含了必要的模糊步骤
    # 在imgGray中查找圆，在canvas中绘制结果
    # canvas必须是shape为[x, y, 3]的图片
    global Hough_x, Hough_y
    img = cv2.medianBlur(imgGray, 3)
    img = cv2.GaussianBlur(img, (17, 19), 0)
    # cv2.imshow("Blur", img)
    # cv2.waitKey(30)
    circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, 200,
                               param1=20, param2=50, minRadius=30, maxRadius=70)
    try:
        # try语法保证在找到圆的前提下才进行绘制
        circles = np.uint16(np.around(circles))
        # print(circles)
        # 经测试，circles为：[[[c0_x, c0_y, c0_r], [c1_x, c1_y, c1_r], ...]]
        # 所以for i in circles[0, :]:中的i为每一个圆的xy坐标和半径
    except:
        pass
    else:
        for i in circles[0, :]:
            # draw the outer circle
            cv2.circle(canvas, (i[0], i[1]), i[2], (255, 100, 0), 2)
            # draw the center of the circle
            cv2.circle(canvas, (i[0], i[1]), 2, (0, 0, 255), 3)
            Hough_x = i[0]
            Hough_y = i[1]

frameWidth = 640
frameHeight = 480
cap = cv2.VideoCapture(0)  # 0对应笔记本自带摄像头
cap.set(3, frameWidth)  # set中，这里的3，下面的4和10是类似于功能号的东西，数字的值没有实际意义
cap.set(4, frameHeight)
cap.set(10, 80)        # 设置亮度
pulse_ms = 30

# 调试用代码，用来产生控制滑条
# cv2.namedWindow("HSV")
# cv2.resizeWindow("HSV", 640, 300)
# cv2.createTrackbar("HUE Min", "HSV", 4, 179, empty)
# cv2.createTrackbar("SAT Min", "HSV", 180, 255, empty)
# cv2.createTrackbar("VALUE Min", "HSV", 156, 255, empty)
# cv2.createTrackbar("HUE Max", "HSV", 32, 179, empty)
# cv2.createTrackbar("SAT Max", "HSV", 255, 255, empty)
# cv2.createTrackbar("VALUE Max", "HSV", 255, 255, empty)
lower = np.array([0, 120, 120])     # 适用于橙色乒乓球4<=h<=32
upper = np.array([250, 255, 255])

targetPos_x = 0     # 颜色检测得到的x坐标
targetPos_y = 0     # 颜色检测得到的y坐标
lastPos_x = 0       # 上一帧图像颜色检测得到的x坐标
lastPos_y = 0       # 上一帧图像颜色检测得到的x坐标
Hough_x = 0         # 霍夫圆检测得到的x坐标
Hough_y = 0         # 霍夫圆检测得到的y坐标
ColorXs = []        # 这些是用来存储x，y坐标的列表，便于后期写入文件
ColorYs = []
HoughXs = []
HoughYs = []

while True:
    img = cv2.imread("pic_.png")
    # _, img = cap.read()
    # 霍夫圆检测前的处理Start
    b, g, r = cv2.split(img)    # 分离三个颜色
    r = np.int16(r)             # 将红色与蓝色转换为int16，为了后期做差
    b = np.int16(b)
    r_minus_b = r - b           # 红色通道减去蓝色通道，得到r_minus_b
    r_minus_b = (r_minus_b + abs(r_minus_b)) / 2    # r_minus_b中小于0的全部转换为0
    r_minus_b = np.uint8(r_minus_b)                 # 将数据类型转换回uint8
    # 霍夫圆检测前的处理End
    imgHough = img.copy()   # 用于绘制识别结果和输出
    imgHsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # h_min = cv2.getTrackbarPos("HUE Min", "HSV")
    # h_max = cv2.getTrackbarPos("HUE Max", "HSV")
    # s_min = cv2.getTrackbarPos("SAT Min", "HSV")
    # s_max = cv2.getTrackbarPos("SAT Max", "HSV")
    # v_min = cv2.getTrackbarPos("VALUE Min", "HSV")
    # v_max = cv2.getTrackbarPos("VALUE Max", "HSV")
    # lower = np.array([h_min, s_min, v_min])
    # upper = np.array([h_max, s_max, v_max])

    imgMask = cv2.inRange(imgHsv, lower, upper)     # 获取遮罩
    imgOutput = cv2.bitwise_and(img, img, mask=imgMask)
    contours, hierarchy = cv2.findContours(imgMask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)   # 查找轮廓
    # https://blog.csdn.net/laobai1015/article/details/76400725
    # CV_RETR_EXTERNAL 只检测最外围轮廓
    # CV_CHAIN_APPROX_NONE 保存物体边界上所有连续的轮廓点到contours向量内
    imgMask = cv2.cvtColor(imgMask, cv2.COLOR_GRAY2BGR)     # 转换后，后期才能够与原画面拼接，否则与原图维数不同

    # 下面的代码查找包围框，并绘制
    x, y, w, h = 0, 0, 0, 0
    X, Y = [], []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        # print(area)
        if area > 300:
            x, y, w, h = cv2.boundingRect(cnt)
            lastPos_x = targetPos_x
            lastPos_y = targetPos_y
            targetPos_x = int(x+w/2)
            targetPos_y = int(y+h/2)
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.circle(img, (targetPos_x, targetPos_y), 2, (0, 255, 0), 4)
        X.append(int(x+w/2))
        Y.append(int(y+h/2))
    # 坐标（图像内的）
    cv2.putText(img, "({:0<2d}, {:0<2d})".format(targetPos_x, targetPos_y), (20, 30),
                cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2)  # 文字
    draw_direction(img, lastPos_x, lastPos_y, targetPos_x, targetPos_y)

    # 霍夫圆检测Start
    Hough_circle(r_minus_b, imgHough)
    cv2.imshow("R_Minus_B", r_minus_b)
    cv2.putText(imgHough, "({:0<2d}, {:0<2d})".format(Hough_x, Hough_y), (20, 30),
                cv2.FONT_HERSHEY_PLAIN, 1, (255, 100, 0), 2)
    # 霍夫圆检测End

    imgStack = np.hstack([img, imgHough])
    # imgStack = np.hstack([img, imgMask])            # 拼接
    cv2.imshow('Horizontal Stacking', imgStack)     # 显示

    ColorXs.append(targetPos_x)     # 坐标存入列表
    ColorYs.append(targetPos_y)
    HoughXs.append(Hough_x)
    HoughYs.append(Hough_y)
    x_hole_center, y_hole_center = int(np.mean(X)), int(np.mean(Y))

    if cv2.waitKey(pulse_ms) & 0xFF == ord('q'):          # 按下“q”推出（英文输入法）
        print("Quit\n")
        break
import pyrealsense2 as rs
import numpy as np
import cv2

pipeline = rs.pipeline()  # pipeline
config = rs.config()  # config
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)  # depth
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)  # color

# config.enable_stream(rs.stream.depth,  848, 480, rs.format.z16, 90)
# config.enable_stream(rs.stream.color, 848, 480, rs.format.bgr8, 30)
# config.enable_stream(rs.stream.depth,  1280, 720, rs.format.z16, 30)
# config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)

pipe_profile = pipeline.start(config)  # streaming流开始

align_to = rs.stream.color  # align_to 
align = rs.align(align_to)  # rs.align 
 
def get_aligned_images():
    frames = pipeline.wait_for_frames() 
    aligned_frames = align.process(frames)
 
    aligned_depth_frame = aligned_frames.get_depth_frame()  # depth
    aligned_color_frame = aligned_frames.get_color_frame()  # color

    depth_intrin = aligned_depth_frame.profile.as_video_stream_profile().intrinsics 
    color_intrin = aligned_color_frame.profile.as_video_stream_profile().intrinsics 
 
    # images to numpy arrays
    img_color = np.asanyarray(aligned_color_frame.get_data())  # RGB
    img_depth = np.asanyarray(aligned_depth_frame.get_data())
 
    return color_intrin, depth_intrin, img_color, img_depth, aligned_depth_frame

def get_3d_camera_coordinate(depth_pixel, aligned_depth_frame, depth_intrin):
    x = depth_pixel[0]
    y = depth_pixel[1]
    dis = aligned_depth_frame.get_distance(x, y)  
    # print ('depth: ',dis) 
    camera_coordinate = rs.rs2_deproject_pixel_to_point(depth_intrin, depth_pixel, dis)
    # print ('camera_coordinate: ',camera_coordinate)
    return dis, camera_coordinate
 
# if __name__ == "__main__":
#     while True:
#         color_intrin, depth_intrin, img_color, img_depth, aligned_depth_frame = get_aligned_images() 
#         depth_pixel = [20, 40]
#         dis, camera_coordinate = get_3d_camera_coordinate(depth_pixel, aligned_depth_frame, depth_intrin)
#         print('depth: ', dis) 
#         print('camera_coordinate: ', camera_coordinate)
#         cv2.circle(img_color, (20, 40), 8, [255, 0, 255], thickness=-1)
#         cv2.putText(img_color, "Dis:" + str(dis) + " m", (40, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.2, [0, 0, 255])
#         cv2.putText(img_color, "X:" + str(camera_coordinate[0]) + " m", (80, 80), cv2.FONT_HERSHEY_SIMPLEX, 1.2,
#                     [255, 0, 0])
#         cv2.putText(img_color, "Y:" + str(camera_coordinate[1]) + " m", (80, 120), cv2.FONT_HERSHEY_SIMPLEX, 1.2,
#                     [255, 0, 0])
#         cv2.putText(img_color, "Z:" + str(camera_coordinate[2]) + " m", (80, 160), cv2.FONT_HERSHEY_SIMPLEX, 1.2,
#                     [255, 0, 0])
#         cv2.imshow('RealSence', img_color)
#         key = cv2.waitKey(1)
def demo(depth_pixel):
    while True:
        color_intrin, depth_intrin, img_color, img_depth, aligned_depth_frame = get_aligned_images() 

        dis, camera_coordinate = get_3d_camera_coordinate(depth_pixel, aligned_depth_frame, depth_intrin)
        print('depth: ', dis) 
        print('camera_coordinate: ', camera_coordinate)
        cv2.circle(img_color, tuple(depth_pixel), 8, [255, 0, 255], thickness=-1)
        cv2.putText(img_color, "Dis:" + str(dis) + " m", (40, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.2, [0, 0, 255])
        cv2.putText(img_color, "X:" + str(camera_coordinate[0]) + " m", (80, 80), cv2.FONT_HERSHEY_SIMPLEX, 1.2,
                    [255, 0, 0])
        cv2.putText(img_color, "Y:" + str(camera_coordinate[1]) + " m", (80, 120), cv2.FONT_HERSHEY_SIMPLEX, 1.2,
                    [255, 0, 0])
        cv2.putText(img_color, "Z:" + str(camera_coordinate[2]) + " m", (80, 160), cv2.FONT_HERSHEY_SIMPLEX, 1.2,
                    [255, 0, 0])
        cv2.imshow('RealSence', img_color)
        key = cv2.waitKey(1)

demo([x_hole_center, y_hole_center])
# filename = 'xy.txt'     # 坐标存入文件

# with open(filename, 'w') as file_object:
#     file_object.write("Color:\n")
#     for i in ColorXs:
#         file_object.write("{:d}\n".format(i))
#     file_object.write("\n***********\n")
#     for i in ColorYs:
#         file_object.write("{:d}\n".format(i))
#     file_object.write("\nHough:\n")
#     for i in HoughXs:
#         file_object.write("{:d}\n".format(i))
#     file_object.write("\n***********\n")
#     for i in HoughYs:
#         file_object.write("{:d}\n".format(i))

# cap.release()
# cv2.destroyAllWindows()
