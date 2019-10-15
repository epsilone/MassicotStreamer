from imutils.video import VideoStream
from cnn_face_detection import FaceDetection
from saving_video import VideoSaver
import numpy as np
import imutils
import time
import cv2

FPS_LIMIT = 1 # Try to see the perf without fps limit
GIF_LENGTH_LIMIT = 15 # The length of the gif video

generate_scream_gif = False
start_time_scream_gif = 0


face_detect = FaceDetection()

print("[INFO] starting video stream...")
cam = cv2.VideoCapture(0)

start_capturing_time = time.time()

while True:
	time_now = time.time()
	# Grap the frame
	_, initial_frame = cam.read()
	initial_frame_dimension = initial_frame.shape[:2]
	frame = imutils.resize(initial_frame, width=400)
	
	if generate_scream_gif:

		if time_now - start_time_scream_gif < GIF_LENGTH_LIMIT:
			video_saver.write_frame(initial_frame)
		else:
			print("[INFO] Release video...")
			video_saver.release_video()
			generate_scream_gif = False
	# We did the detection only on 1 frame by second
	elif (int(time_now - start_capturing_time)) > FPS_LIMIT: 
		frame_resized = cv2.resize(frame, (300, 300))
		
		detections = face_detect.generate_detections(frame_resized)

		for i in range(0, detections.shape[2]):
			detection_confidence = detections[0, 0, i, 2]

			if detection_confidence < face_detect.confidence:
				continue
			print("[INFO] Saving video...")
			start_time_scream_gif = time.time()
			generate_scream_gif = True
			video_saver = VideoSaver()
			# TODO :  May we wait something like 2s before starting the sound and blow air
			# Like that We'll have the full reactiong
			# Start sound
			# Start blowing air
	# comment these 3 lines if you're run this on the raspberry
	cv2.imshow('Preview', frame) 
	if cv2.waitKey(1) & 0xFF == ord('c'):
		break

cv2.destroyAllWindows()
cam.stop()