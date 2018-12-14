import os
from collections import Counter,defaultdict
import pickle
import json
from shutil import copyfile as copy
from pathlib import Path

with open("subjects_tag_id_map.pickle","rb") as fl:
    subjects_tag_id_map = pickle.load(fl)

for subject in subjects_tag_id_map:
    for songlist in subjects_tag_id_map[subject]:
        for x in range(len(subjects_tag_id_map[subject][songlist])):
            subjects_tag_id_map[subject][songlist][x]=list(subjects_tag_id_map[subject][songlist][x])

for subject in subjects_tag_id_map:
    for songlist in subjects_tag_id_map[subject]:
        for x in range(len(subjects_tag_id_map[subject][songlist])):
            if subjects_tag_id_map[subject][songlist][x][1]=="other":
                subjects_tag_id_map[subject][songlist][x][1]="not-funny"
for subject in subjects_tag_id_map:
    for songlist in subjects_tag_id_map[subject]:
        for x in range(len(subjects_tag_id_map[subject][songlist])):
            if subjects_tag_id_map[subject][songlist][x][1]=="not-funny":
                subjects_tag_id_map[subject][songlist][x][1]="not_funny"

final_tag=defaultdict(lambda: defaultdict(str))
audio_id = defaultdict(lambda: defaultdict(int))
temp=defaultdict(lambda: defaultdict(list))
for subject in subjects_tag_id_map:
    for songlist in subjects_tag_id_map[subject]:
        for songs in subjects_tag_id_map[subject][songlist]:
            songs = tuple(songs)
            temp[songlist][songs].append(songs[1])

for songlist in temp:
    for songs in temp[songlist]:
        temp[songlist][songs]=Counter(temp[songlist][songs])
for songlist in temp:
    for songs in temp[songlist]:
        for label in temp[songlist][songs]:
            if temp[songlist][songs][label]>1:
                final_tag[songlist][songs[2]]=label
                audio_id[songlist][songs[2]]=songs[0]

script_path = os.path.dirname(os.path.abspath(__file__))
data_path=os.path.join(script_path,"data_v1")
audio_data_path = os.path.join(script_path,"trimmed_audio")

out_path=os.path.join(script_path,"data_v2/lyrics")
audio_path =os.path.join(script_path,"data_v2/audio")

audio_funny_path = os.path.join(audio_path,"funny")
audio_not_funny_path = os.path.join(audio_path,"not_funny")

funny_path = os.path.join(out_path,"funny")
not_funny_path = os.path.join(out_path,"not_funny")

if not os.path.exists(audio_path):
    os.makedirs(audio_path)
if not os.path.exists(audio_funny_path):
    os.makedirs(audio_funny_path)
if not os.path.exists(audio_not_funny_path):
    os.makedirs(audio_not_funny_path)

if not os.path.exists(out_path):
    os.makedirs(out_path)
if not os.path.exists(funny_path):
    os.makedirs(funny_path)
if not os.path.exists(not_funny_path):
    os.makedirs(not_funny_path)

def get_id(song_name,type):
    if not isinstance(type,list):
        if song_name in final_tag[type]:
            return audio_id[type][song_name],type
    else:
        if song_name in audio_id[type[0]]:
            return audio_id[type[0]][song_name],type[0]
        if song_name in audio_id[type[1]]:
            return audio_id[type[1]][song_name],type[1]
    return 0

def get_label(song_name,type):
    if not isinstance(type,list):
        if song_name in final_tag[type]:
            return final_tag[type][song_name]
    else:
        if song_name in final_tag[type[0]]:
            return final_tag[type[0]][song_name]
        if song_name in final_tag[type[1]]:
            return final_tag[type[1]][song_name]
    return 0


for file in sorted(os.listdir(data_path)):
    if file.split("_")[0]=="u": ##means unmatched song_name file
        type="_".join(file.split("_")[1:-1])
        song_name = file.split("_")[-1].split(".txt")[0].strip()
        assert type=="5th_sem"
        types=type+"_songs"
        lines = open(os.path.join(data_path,file),"r").readlines()
        assert len(lines)==4
        lyrics = lines[3]
        label = get_label(song_name,types)
        id,type_ = get_id(song_name,types)
        if label and id:
            audio_file_path = audio_funny_path if label=="funny" else audio_not_funny_path
            copy(os.path.join(os.path.join(audio_data_path,type_),str(id)+".mp3"),os.path.join(audio_file_path,"u_"+song_name+".mp3"))
            lyrics_file_path = funny_path if label=="funny" else not_funny_path
            #Path(lyrics_file_path+"/u_"+song_name+".txt").touch()
            fd = open(lyrics_file_path+"/u_"+song_name+".txt","w")
            fd.write(lyrics)
            fd.close()
    else:
        type="_".join(file.split("_")[1:-1])
        song_name = file.split("_")[-1].split(".txt")[0].strip()
        assert type in ("lb_new","5th_sem")
        if type=="lb_new":
            types=["lb_songs","new_songs"]
        else:
            types = "5th_sem_songs"
        ##lyrics extraction
        lyrics = open(os.path.join(data_path,file),"r").readlines()[0].split("[")[1].split("]")[0].strip()
        segments = lyrics.split(",")
        lyrc = segments[0].strip().split('\\n')[0].replace("'","")
        for segment in segments[1:]:
        	if len(segment.strip().split('\\n'))>1:
        		lyrc+="\n"+segment.strip().split('\\n')[1].replace("'","")
        	else:
        		lyrc+="\n\n"+segment.strip().split('\\n')[0].replace("'","")
        formatted_lyrc=lyrc
        label = get_label(song_name,types)
        id,type_ = get_id(song_name,types)
        #print(id,type_)
        if label and id:
            audio_file_path = audio_funny_path if label=="funny" else audio_not_funny_path
            lyrics_file_path = funny_path if label=="funny" else not_funny_path
            copy(os.path.join(os.path.join(audio_data_path,type_),str(id)+".mp3"),os.path.join(audio_file_path,"m_"+song_name+".mp3"))
            #Path(lyrics_file_path+"/m_"+song_name+".txt").touch()
            fd = open(lyrics_file_path+"/m_"+song_name+".txt","w")
            fd.write(formatted_lyrc)
            fd.close()
