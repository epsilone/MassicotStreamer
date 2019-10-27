from imutils.video import VideoStream
from cnn_face_detection import FaceDetection
from saving_video import VideoSaver
from guillotinehw import GuillotineHW
import numpy as np
import imutils
import time
import cv2

FPS_LIMIT = 1 # Try to see the perf without fps limit
GIF_LENGTH_LIMIT = 15 # The length of the gif video
TIME_BEFORE_SOUND = 5

video_saver = None
face_detect = FaceDetection()
guillotine = GuillotineHW()

print("[INFO] starting video stream...")
cam = cv2.VideoCapture(0)

last_capturing_time = 0
face_detected_time = 0
waiting_for_air = 0
time_to_stop_air = 0


while True:
    time_now = time.time()
    # Grap the frame
    _, initial_frame = cam.read()
    initial_frame_dimension = initial_frame.shape[:2]
    frame = imutils.resize(initial_frame, width=400)

    if video_saver:
        time_since_detection = time_now - face_detected_time
        # We are recording the face
        if time_since_detection < GIF_LENGTH_LIMIT:
            video_saver.write_frame(frame)
        else:
            video_saver.release_video()
            video_saver = None
            face_detected_time = 0
            waiting_for_air = 0

        # State machine for hardware.
        if not waiting_for_air and time_since_detection > TIME_BEFORE_SOUND:
            waiting_for_air = time_since_detection + guillotine.start_sound()

        if waiting_for_air and time_since_detection > waiting_for_air:
            time_to_stop_air = time_since_detection + guillotine.start_air()
            waiting_for_air = 0

        if time_to_stop_air and time_since_detection > time_to_stop_air:
            guillotine.stop_air()
            time_to_stop_air = 0

    elif (int(time_now - last_capturing_time)) > FPS_LIMIT:
        # Only try to detect every 1s.
        last_capturing_time = time_now
        frame_resized = cv2.resize(frame, (300, 300))

        detections = face_detect.generate_detections(frame_resized)

        for i in range(0, detections.shape[2]):
            detection_confidence = detections[0, 0, i, 2]
            if detection_confidence < face_detect.confidence:
                continue
            print("[INFO][CAMERA] Start saving video...")
            face_detected_time = time_now
            video_saver = VideoSaver()
            # we found a face!
            break
    # comment these 3 lines if you're run this on the raspberry
    # cv2.imshow('Preview', frame)
    # if cv2.waitKey(1) & 0xFF == ord('c'):
    #    break

cv2.destroyAllWindows()
cam.stop()
