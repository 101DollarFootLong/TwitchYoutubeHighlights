import os
from moviepy.editor import *
from PIL import ImageFont, ImageDraw
from moviepy.video.io.bindings import PIL_to_npimage
import PIL.Image as plim
import shutil

# Need to instal ImageMagick and add it to path 'IMAGEMAGICK_BINARY'
clips = []

os.chdir(os.path.dirname(os.path.realpath(__file__)))
video_path = os.getcwd().replace('core', 'DownloadedVideos')
print(video_path)

os.chdir(video_path)
for filename in os.listdir("."):
    if filename.endswith(".mp4"):
        #textclip = VideoClip(makeframe("test"), duration=36)
        clip = VideoFileClip(filename)
        creator_name = filename.split("_")[0]
        # TODO: Use PIL to speed up the text render process
        # 5 clips: 47mins
        #textclip = TextClip(creator_name, fontsize=60, color='white').set_pos(("right", "bottom")).set_duration(int(clip.duration))
        
        #final_clip = CompositeVideoClip([clip,textclip])
        #clips.append(final_clip)
        clips.append(clip)

video = concatenate_videoclips(clips, method='compose')
render_video = "render.mp4"
video.write_videofile(render_video)
shutil.move(video_path+"\\"+render_video, video_path+"\\"+"Rendered"+ "\\" + render_video)

# https://gist.github.com/Zulko/06f49f075fd00e99b4e6#file-moviepy_time_accuracy-py-L33-L39