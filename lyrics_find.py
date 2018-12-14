import os
import pickle
from collections import Counter
from collections import defaultdict
from difflib import SequenceMatcher
import json
from shutil import copyfile as copy

with open("subjects_tag_id_map.pickle","rb") as fl:
    subjects_tag_id_mapping = pickle.load(fl)

tag_id_map = subjects_tag_id_mapping["first"]
song_names=[]
old_work_song_names=[]
for songlist in tag_id_map:
    if songlist!="5th_sem_songs":
        for id,tag,song_name in tag_id_map[songlist]:
            if song_name:
                song_names.append(song_name)
            else:
                print("opps!!!")
    else:
        for id,tag,song_name in tag_id_map[songlist]:
            if song_name:
                old_work_song_names.append(song_name)
            else:
                print("opps!!!")
raw_data={
"lb_new":song_names,
"5th_sem":[name for name in old_work_song_names if name not in song_names]
}
l=0
if len(song_names)==len(list(set(song_names))):
    print("No duplicates in lb_songs and new_songs")
    print(len(song_names))
if len(old_work_song_names)==len(list(set(old_work_song_names))):
    print("No duplicates in 5th_sem_songs")
    print(len(old_work_song_names))
if bool(set(song_names) & set(old_work_song_names)):
    print("Duplicate songs in both songlists: ",list(set(song_names) & set(old_work_song_names)))
    #duplicates = list(set(song_names) & set(old_work_song_names))
    temp=[]
    temp.extend(song_names)
    temp.extend(old_work_song_names)
    print("Total songs in dataset: ",len(temp))
    temp =list(set(temp))
    print("Total songs in dataset: (after duplicate removal)",len(temp))
if not bool(set(song_names) & set(old_work_song_names)):
    print("No duplicate songs in both songlists")
    temp=[]
    temp.extend(song_names)
    temp.extend(old_work_song_names)
    print("Total songs in dataset: (no presence of duplicate instances)",len(temp))

print("\n\nSanity Checks...\n\n")
if len(raw_data["lb_new"])+len(raw_data["5th_sem"])==len(temp):
    print("Check passed!!!")
    print(len(raw_data["lb_new"]),len(raw_data["5th_sem"]))
funny_songs_data="funny/"
script_path = os.path.dirname(os.path.abspath(__file__))
funny_songs=[]
for file in os.listdir(os.path.join(script_path,funny_songs_data)):
    name = file.split("_")[-1].split(".csv")[0].strip()
    movie_date = file.split("_")[0].strip()
    if (name,movie_date) not in funny_songs:
        funny_songs.append((name,movie_date))

print("\n\nTotal funny songs present on lyricsbogie.com: ",len(funny_songs),"\n\n")

def longestSubstring(str1,str2):
    # initialize SequenceMatcher object with
    # input string
    seqMatch = SequenceMatcher(None,str1,str2)
    # find match of longest sub-string
    # output will be like Match(a=0, b=0, size=5)
    match = seqMatch.find_longest_match(0, len(str1), 0, len(str2))
    # print longest substring
    if (match.size!=0):
        return str1[match.a: match.a + match.size]
    else:
        return None
match=defaultdict(list)
all_songs_lower = [(name.lower(),name) for name in temp]
funny_songs_lower = [(name.lower(),date) for name,date in funny_songs]
for name1,date in funny_songs_lower:
    for name2_lower,name2 in all_songs_lower:
        if name1==name2_lower:
            type = "lb_new" if name2 in raw_data["lb_new"] else "5th_sem"
            #print(name1+"-----"+name2)
            match[type].append((date,name1,name2))
s=0
for item in match.values():
    s+=len(item)
print("Total fully matched songs: ",s,"\n")

for type in match:
    print("total songs of type: "+type+" - "+str(len(raw_data[type])))
    print("matched songs of type: "+type+" - "+str(len(match[type])))
    print("umatched songs of type: "+type+" - "+str(len(raw_data[type])-len(match[type])))
    print("\n")

unmatch=defaultdict(list)
for type in raw_data:
    for song_name in raw_data[type]:
        tmp=[match_name for _,_,match_name in match[type]]
        if song_name not in tmp:
            unmatch[type].append(song_name)
for type in raw_data:
    output_path=os.path.join(script_path,"data_v1")
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    matched_song_names = [name for _,_,name in match[type]]
    matched_song_info = [(date,orig_song_file_name) for date,orig_song_file_name,_ in match[type]]
    for song_name in raw_data[type]:
        if song_name in matched_song_names:
            for x in range(len(matched_song_names)):
                song_name = matched_song_names[x]
                for file in os.listdir(os.path.join(script_path,"funny")):
                    if matched_song_info[x][0]==file.split("_")[0].strip() and matched_song_info[x][1]==file.split("_")[-1].split(".csv")[0].strip().lower():
                        copy(os.path.join(os.path.join(script_path,"funny"),file),os.path.join(output_path,"m_"+type+"_"+song_name+".txt"))

        else:
            if type=="5th_sem":
                for file in os.listdir(os.path.join(script_path,"5th_sem_songs_lyrics")):
                    name =open(os.path.join(os.path.join(script_path,"5th_sem_songs_lyrics"),file),"r").readline().strip()
                    name = name.split("-")[0].strip() if "-" in name else name
                    if name==song_name:
                        copy(os.path.join(os.path.join(script_path,"5th_sem_songs_lyrics"),file),os.path.join(output_path,"u_"+type+"_"+song_name+".txt"))
