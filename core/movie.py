import os
from moviepy.editor import *
import shutil

os.chdir(os.path.dirname(os.path.realpath(__file__)))
print(f"Upload_video.py: {os.getcwd()}")
#dir = os.chdir(os.getcwd().replace('core', 'DownloadedVideos'))

def text_editor(text_pos):
    clips = []
    for filename in os.listdir("."):
        if filename.endswith(".mp4") and "_text" not in filename:
            creator_name = filename.split("_")[0]
            font = '../Dependencies/Metropolis Black.ttf'
            twitchstreamerstr= "Twitch\: {0}".format(creator_name.title())
            output_name = filename.split(".mp4")[0] + "_text.mp4" 
            # Add ffmpeg into the PATH
            script = "ffmpeg -i {0} -vf drawtext=\"fontfile={1}:fontsize=35: fontcolor=white:shadowcolor=black:shadowx=2:shadowy=2:{2}:text='{3}'\" {4}".format(filename,font,text_pos,twitchstreamerstr,output_name)
            print("Running Script...")
            os.system(script)
            text_clip = VideoFileClip(output_name)
            clips.append(text_clip)
    return clips

def render(text_pos):
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    dir = os.chdir(os.getcwd().replace('core', 'DownloadedVideos'))
    print(f"Upload_video.py: {os.getcwd()}")

    clips = text_editor(text_pos)
    video = concatenate_videoclips(clips, method='compose')
    render_video = "render.mp4"
    video.write_videofile(render_video)
    shutil.move(render_video,"..\\Rendered"+ "\\" + render_video)

#https://learndataanalysis.org/how-to-upload-a-video-to-youtube-using-youtube-data-api-in-python/