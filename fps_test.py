from camera import VideoCam
import time

fpsLimit = 1 # throttle limit
camera_ext = VideoCam()
startTime = time.time()
while True:
    ret = camera_ext.cap.grab()
    nowTime = time.time()
    if (int(nowTime - startTime)) > fpsLimit:
        ret, frame = camera_ext.get_frame()
        camera_ext.show_frame(frame, 'frame')
camera_ext.close_cam()
