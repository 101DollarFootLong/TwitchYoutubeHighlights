import os
from moviepy.editor import *
import shutil
import random

def text_editor(text_pos):
    print(f"text_editor: {os.getcwd()}")
    clips = []
    for filename in os.listdir("."):
        if filename.endswith(".mp4") and "_text" not in filename:
            creator_name = filename.split("_")[0]
            # Change the path to the 
            font_path = "../../core/dependencies/Metropolis Black.ttf"
            twitchstreamerstr= "Twitch\: {0}".format(creator_name.title())
            output_name = filename.split(".mp4")[0] + "_text.mp4" 
            # Add ffmpeg into the PATH
            
            # Check for the correct 1080X1920
            clip = VideoFileClip(filename)
            if clip.w == 1920:
                input_file = filename
            else:
                clip_resized = clip.resize(newsize=(1920,1080))
                input_file = f"{filename}_resized.mp4"
                clip_resized.write_videofile(input_file)

            script = "ffmpeg -i {0} -vf drawtext=\"fontfile='{1}':fontsize=35: fontcolor=white:shadowcolor=black:shadowx=2:shadowy=2:{2}:text='{3}'\" {4}".format(input_file,font_path,text_pos,twitchstreamerstr,output_name)
            print("Running Script...")
            os.system(script)

            text_clip = VideoFileClip(output_name)
            clips.append(text_clip)
    # return a shuffled version of the videos 
    return random.shuffle(clips)

def render(render_video, text_pos):
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    path = os.getcwd().replace('core\\bin', 'videos\\Downloaded')
    dir = os.chdir(path)
    print(f"Upload_video.py: {os.getcwd()}")
    clips = text_editor(text_pos)
    video = concatenate_videoclips(clips, method='compose')
    video.write_videofile(render_video)
    shutil.move(render_video,"..\\Rendered"+ "\\" + render_video)

