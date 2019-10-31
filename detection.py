from cnn_face_detection import FaceDetection
import imutils
import cv2


class CameraDetection(object):
    def __init__(self, debug=False):
        print("[INFO] starting video detection.")
        self.cam = cv2.VideoCapture(0)
        self.face_detect = FaceDetection()
        self.debug = debug

    def get_frame(self):
        _, initial_frame = self.cam.read()
        initial_frame_dimension = initial_frame.shape[:2]
        frame = imutils.resize(initial_frame, width=400)
        return frame

    def is_face_detected(self, frame):
        if self.debug:
            cv2.imshow('Preview', frame)
            if cv2.waitKey(1) & 0xFF == ord('c'):
                return False
        frame_resized = cv2.resize(frame, (300, 300))
        detections = self.face_detect.generate_detections(frame_resized)
        for i in range(0, detections.shape[2]):
            detection_confidence = detections[0, 0, i, 2]
            if detection_confidence >= self.face_detect.confidence:
                print("[INFO] client in the hole.")
                return True
        return False

    def __del__(self):
        cv2.destroyAllWindows()
        self.cam.release()
