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

# Need to instal ImageMagick and add it to path 'IMAGEMAGICK_BINARY'
# Add ffmpeg into the PATH
clips = []

os.chdir(os.path.dirname(os.path.realpath(__file__)))
os.chdir(os.getcwd().replace('core', 'DownloadedVideos'))

for filename in os.listdir("."):
    if filename.endswith(".mp4") and "_text" not in filename:
        creator_name = filename.split("_")[0]
        font = 'Metropolis Black.ttf'
        twitchstreamerstr= f"TwichStreamer{creator_name}"
        #top_right = "x=w-tw-10:y=10"
        bottom_right = "x=w-tw-10:y=h-th-10"
        output_name = filename.split(".mp4")[0] + "_text.mp4" 
        script = f'ffmpeg -i {filename} -vf drawtext="fontfile={font}:fontsize=35: fontcolor=white:{bottom_right}:text="{twitchstreamerstr}""  {output_name}"'
        print("Running Script...")
        os.system(script)
        text_clip = VideoFileClip(output_name)
        clips.append(text_clip)

video = concatenate_videoclips(clips, method='compose')
render_video = "render.mp4"
video.write_videofile(render_video)
shutil.move(render_video,"Rendered"+ "\\" + render_video)