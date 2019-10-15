# MassicotStreamer
Automation of a Guillotine.
Scare people and broadcast to the world.

## Goal
1. Detect when a face enters the Guillotine
2. Trigger the Guillotine mechanism (Without killing the subject)
3. Stream the reaction of the subject on social media

## Steps
1. Play the Guillotine sound
* Regular interval
* The speakers will be placed being the head of the subject. He won't be able to tell if the blades is actually coming down on hom or not.
2. Capture the video
* Stream it directly on social media
3. Detecting a face
* Upon detection, triggering the sound
* Upon detection, triggering the creation of an animated gif and uploading the said gif to the cloud
* Upon detection, triggering a relay to blast air draft unto subject neck


## Raspberry

login=pi
pwd=raspberry


### OpenCV
If you want to use OpenCV on the raspberry you'll need to compile OpenCV by hand, cause using pip is not working.

Just follow step by step this tutorial : https://linuxize.com/post/how-to-install-opencv-on-raspberry-pi/

### Run

```
$ python3 face_detection_camera.py
```

### WIFI
Change the login and password of the WIFI after ssh in the raspberry.
```
$ sudo nano /etc/wpa_supplicant/wpa_supplicant.conf
```

### Streaming
https://www.raspberrypi.org/forums/viewtopic.php?t=133871#p1011437

ffmpeg -thread_queue_size 512 -f v4l2 -i /dev/video1 \
  -ar 44100 -ac 2 -acodec pcm_s16le -f s16le -ac 2 -i /dev/zero -acodec aac -ab 128k -strict experimental \
  -aspect 16:9 -vcodec h264 -preset veryfast -crf 25 -pix_fmt yuv420p -g 60 -vb 820k -maxrate 820k -bufsize 820k -profile:v baseline \
  -r 30 -f flv rtmp://a.rtmp.youtube.com/live2/[YOUTUBE_KEY]
  
Try to use https://github.com/umlaeute/v4l2loopback to simulate the camera on 2 endpoints and be able to use it on 2 differents process :
  - ffmpeg : Streaming
  - python opencv : Face detection