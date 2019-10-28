from detection import CameraDetection
from guillotinehw import GuillotineHW
from saving_video import VideoSaver

# ------------------- SYNC TIME ------------------- #
TIME_STEP_CONFIRMED_CLIENT = 3  # we can start recording after 3s of confirmed step as if there was a clear picture.
TIME_BETWEEN_CONFIRMED_AND_SOUND = 3  # 3s after a face detection or a step confirmed
TIME_AFTER_CHOPPED = 5
# ------------------------------------------------- #

# STATES
NO_CLIENT = 1
CLIENT_STEP_ONLY = 2
CLIENT_CONFIRMED = 3
SOUND_PLAYING = 4
AIR_PUSHING = 5 
HEAD_CHOPPED = 6


class Guillotine(object):
    def __init__(self):
        self.hw = GuillotineHW()
        self.camera = CameraDetection()
        self.init_guillotine()

    def init_guillotine(self):
        self.time_to_next = 0
        self.video_saver = None
        self.state = NO_CLIENT

    def detect_face(self, now, frame):
        face_detected = self.camera.is_face_detected(frame)
        if face_detected:
            self.we_have_a_client(now, fame)
            return True
        return False

    def we_have_a_client(self, now, frame):
        self.state = CLIENT_CONFIRMED
        self.video_saver = VideoSaver()
        self.video_saver.write_frame(frame)
        self.time_to_next = now + TIME_BETWEEN_CONFIRMED_AND_SOUND

    def game_loop(self):
        frame = self.camera.get_frame()
        now = time.time()
        if state == NO_CLIENT:
            if self.detect_face(now, frame):
                continue
            elif self.hw.is_step_detected():
                self.time_to_next = now + TIME_STEP_CONFIRMED_CLIENT
                self.state = CLIENT_STEP_ONLY
                continue
        elif self.state == CLIENT_STEP_ONLY:
            if self.detect_face(now, frame):
                # if we find a face, stop looking for the feet.
                continue
            if self.hw.is_step_detected():
                if now > self.time_to_next:
                    self.we_have_a_client(now, frame)
            else:
                # client is not there anymore
                # or it was a fluck
                self.init_guillotine()
                continue
        elif self.state == CLIENT_CONFIRMED:
            self.video_saver.write_frame(frame)
            # We are waiting that client is confortable.
            if now > self.time_to_next:
                self.time_to_next = now + self.hw.start_sound()
                self.state = SOUND_PLAYING
        elif self.state == SOUND_PLAYING:
            self.video_saver.write_frame(frame)
            if now > self.time_to_next:
                self.time_to_next = now + self.hw.start_air()
                self.state = AIR_PUSHING
        elif self.state == AIR_PUSHING:
            self.video_saver.write_frame(frame)
            if now > self.time_to_next:
                self.hw.stop_air()
                self.time_to_next = now + TIME_AFTER_CHOPPED
                self.state = HEAD_CHOPPED
        elif self.state == HEAD_CHOPPED:
            self.video_saver.write_frame(frame)
            if now > self.time_to_next:
                self.video_saver.release_video()

    def __del__(self):
        if self.video_saver:
            self.video_saver.release_video()

gui = Guillotine()
while True:
	gui.game_loop()
