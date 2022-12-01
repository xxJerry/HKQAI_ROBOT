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
 
if __name__ == "__main__":

    for i in range(10):
        color_intrin, depth_intrin, img_color, img_depth, aligned_depth_frame = get_aligned_images() 
    depth_pixel = [400, 300]
    dis, camera_coordinate = get_3d_camera_coordinate(depth_pixel, aligned_depth_frame, depth_intrin)
    # print('depth: ', dis) 
    # print('camera_coordinate: ', camera_coordinate)
    # cv2.circle(img_color, (320, 240), 8, [255, 0, 255], thickness=-1)
    # cv2.putText(img_color, "Dis:" + str(dis) + " m", (40, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.2, [0, 0, 255])
    # cv2.putText(img_color, "X:" + str(camera_coordinate[0]) + " m", (80, 80), cv2.FONT_HERSHEY_SIMPLEX, 1.2,
    #             [255, 0, 0])
    # cv2.putText(img_color, "Y:" + str(camera_coordinate[1]) + " m", (80, 120), cv2.FONT_HERSHEY_SIMPLEX, 1.2,
    #             [255, 0, 0])
    # cv2.putText(img_color, "Z:" + str(camera_coordinate[2]) + " m", (80, 160), cv2.FONT_HERSHEY_SIMPLEX, 1.2,
    #             [255, 0, 0])
    cv2.imshow('RealSence', img_color)
    key = cv2.waitKey(10000)
    print(key)


    if key == ord('s'):  # 按下s键，进入下面的保存图片操作
        cv2.imwrite("pic.png", img_color)
        print("save" + " pic.png successfuly!")
        print("-------------------------")

    elif key == ord('q'):  # 按下q键，程序退出
        pass

    cv2.destroyAllWindows()# 释放并销毁窗口
