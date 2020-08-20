import os
from moviepy.editor import *
from PIL import ImageFont, ImageDraw
from moviepy.video.io.bindings import PIL_to_npimage
import PIL.Image as plim
import shutil

def makeframe(t):
    im = plim.new('RGB',(200,100))
    draw = ImageDraw.Draw(im)
    draw.text((50, 25), t)
    return PIL_to_npimage(im)

# Add ffmpeg into the PATH
clips = []

os.chdir(os.path.dirname(os.path.realpath(__file__)))
os.chdir(os.getcwd().replace('core', 'DownloadedVideos'))

# Ideal positions: Fall guy - topcenter | League - topleft
position = {"topleft":"x=10:y=10",
            "topcenter":"x=(w-text_w)/2:y=10",
            "topright":"x=w-tw-10:y=10",
            "center":"x=(w-text_w)/2:y=(h-text_h)/2",
            "bottomleft":"x=10:y=h-th-10",
            "bottomcenter":"x=(w-text_w)/2:y=h-th-10",
            "bottomright":"x=w-tw-10:y=h-th-10"}
for filename in os.listdir("."):
    if filename.endswith(".mp4") and "_text" not in filename:
        creator_name = filename.split("_")[0]
        font = '../Dependencies/Metropolis Black.ttf'
        twitchstreamerstr= "Twitch\: {0}".format(creator_name.title())
        output_name = filename.split(".mp4")[0] + "_text.mp4" 
        script = "ffmpeg -i {0} -vf drawtext=\"fontfile={1}:fontsize=35: fontcolor=white:shadowcolor=black:shadowx=2:shadowy=2:{2}:text='{3}'\" {4}".format(filename,font,position["topleft"],twitchstreamerstr,output_name)
        print("Running Script...")
        os.system(script)
        text_clip = VideoFileClip(output_name)
        clips.append(text_clip)

# video = concatenate_videoclips(clips, method='compose')
# render_video = "render.mp4"
# video.write_videofile(render_video)
# shutil.move(render_video,"..\\Rendered"+ "\\" + render_video)