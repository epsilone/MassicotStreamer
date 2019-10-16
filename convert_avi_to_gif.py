from os import system, walk
from os.path import join, dirname, realpath
videos_path = join(dirname(realpath(__file__)), 'videos/')
video_files = []
for (dirpath, dirnames, filenames) in walk(videos_path):
    video_files.extend([file for file in filenames if file[0] != "." and file.split(".")[1] == "avi"])
    break

for video in video_files:
    video_name = video.split(".")[0]
    convert_to_gif = "ffmpeg -i {0}.avi {0}.gif -hide_banner".format(video_name)
    remove_avi = "rm {}".format(video)
    print(convert_to_gif)
    print(remove_avi)
    # system(convert_to_gif)
    # system(remove_avi)