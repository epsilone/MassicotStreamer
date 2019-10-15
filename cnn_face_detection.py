import cv2

class FaceDetection:
    def __init__(self):
        self.prototxt = "model/deploy.prototxt.txt"
        self.model = "model/res10_300x300_ssd_iter_140000.caffemodel"
        self.confidence = 0.7
        print("[INFO][FACE] loading model...")
        self.net = cv2.dnn.readNetFromCaffe(self.prototxt, self.model)

    def generate_detections(self, frame):
        # pass the blob through the network and obtain the detections and
        # predictions
        blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))
        self.net.setInput(blob)
        return self.net.forward()