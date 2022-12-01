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
