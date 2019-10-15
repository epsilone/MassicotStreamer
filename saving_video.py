import cv2
import datetime
from os.path import join, dirname, realpath

UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'videos/')

class VideoSaver:
    def __init__(self, fps=20, codec=["M", "J", "P", "G"]):
        self.output = self.generate_video_file_name()
        self.fps = fps
        self.codec = codec
        self.fourcc = cv2.VideoWriter_fourcc(*self.codec)
        self.writer = None
        self.h, self.w = (None, None)

    def write_frame(self, frame):
        # check if the writer is None
        if self.writer is None:
            self.h, self.w = frame.shape[:2]
            self.writer = cv2.VideoWriter(self.output, self.fourcc, self.fps, (self.w, self.h), True)
        self.writer.write(frame) 

    def release_video(self):
        self.writer.release()

    def generate_video_file_name(self):
        now = datetime.datetime.now()
        return join( UPLOAD_FOLDER, "video_{}.avi".format(now.isoformat()) )