# Add ffmpeg into the PATH
import os
from moviepy.editor import *
import shutil
import random
import time

def text_editor(text_pos):
    print(f"text_editor: {os.getcwd()}")
    clips = []
    creator_names = []
    video_durations = []
    for filename in os.listdir("."):
        if filename.endswith(".mp4") and "_text" not in filename:
            creator_name = filename.split("_")[0]
            # Change the path to the 
            font_path = "../../core/dependencies/Metropolis Black.ttf"
            twitchstreamerstr= "Twitch\: {0}".format(creator_name.title())
            output_name = filename.split(".mp4")[0] + "_text.mp4" 

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

            # add the infos into the lists
            creator_names.append(creator_name)
            video_durations.append(clip.duration)
            clip.close()
    
    timer_dict = description_timers(creator_names,video_durations)

    # return a shuffled version of the videos, and the dictionary of video durations and creator names
    return clips, timer_dict

def render(render_video, text_pos):
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    path = os.getcwd().replace('core\\bin', 'videos\\Downloaded')
    dir = os.chdir(path)
    clips, timer_dict = text_editor(text_pos)
    video = concatenate_videoclips(clips, method='compose')
    video.write_videofile(render_video)
    shutil.move(render_video,"..\\Rendered"+ "\\" + render_video)
    video.close()
    return timer_dict

def description_timers(creator_name,time_length):
    creator_name_dict = {}
    previous_time = 0
    for i in range(0,len(creator_name)):
        # print(f"i: {i} pre: {previous_time} current: {time_length[i]}")
        if creator_name[i] not in creator_name_dict:
            creator_name_dict[creator_name[i]] = (time_length[i] + previous_time)
        else:
            creator_name_dict[creator_name[i]] += time_length[i] 
        previous_time += time_length[i] 
    # Change the seconds into minutes:seconds format
    times_format = list(map(lambda x: time.strftime("%M:%S",time.gmtime(x)), creator_name_dict.values()))
    return dict(zip(creator_name_dict.keys(), times_format))