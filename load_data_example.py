#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 27 10:20:04 2020

@author: pomchi
"""

import pyrealsense2 as rs
import numpy as np
import cv2


pipeline = rs.pipeline()
config = rs.config()

filepath = './20200826_112829.bag'
rs.config.enable_device_from_file(config,filepath)

#(depth/RGB,W,H,value type,fps)
config.enable_stream(rs.stream.depth,640,480,rs.format.z16,30)

# start loading data
pipeline.start(config)
colorizer = rs.colorizer();
count = 0
while True:
    # Get frameset of depth
    frames = pipeline.wait_for_frames()

    # Get depth frame
    depth_frame = frames.get_depth_frame()

    # Convert to Numpy Array
    frame = np.asanyarray(depth_frame.get_data())

    # Colorize depth frame to jet colormap
    depth_color_frame = colorizer.colorize(depth_frame)

    # Convert depth_frame to numpy array to render image in opencv
    depth_frame = np.asanyarray(depth_frame.get_data())
    ###
    # depth_frame = (depth_frame/256).astype('uint8')
    # print(depth_frame.shape)
    # print(depth_frame)
    ###
    depth_color_image = np.asanyarray(depth_color_frame.get_data())

    # Render image in opencv window
    # cv2.imshow("Depth Stream", depth_frame)
    if count%30==0:
        cv2.imwrite("./result/fram%06d.png" % count, depth_color_image)
        cv2.imwrite("./result2/fram%06d.png" % count, depth_frame)
    count+=1
    # break
    key = cv2.waitKey(1)
    if key == 27:
        cv2.destroyAllWindows()
        break
