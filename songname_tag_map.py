import os
import pickle
from collections import Counter,defaultdict
script_path = os.path.dirname(os.path.abspath(__file__))
audio_data_path = script_path+"/trimmed_audio/"
songs_list=["lb_songs.txt","new_songs.txt","5th_sem_songs.txt"]
songs_ids={}
for songlist in songs_list:
    filename = os.path.join(script_path,songlist)
    temp=[]
    songs = open(filename,"r").readlines()
    #print(songs)
    for song in songs:
        song_id = int(song.split('"')[0].strip())
        song_name = song.split('"')[1].strip()
        song_name = song_name.split("-")[0].strip() if "-" in song_name else song_name
        temp.append((song_id,song_name))
    temp.sort(key=lambda x:x[0])
    songs_ids[songlist.split(".")[0]] = temp
for songlist in songs_ids:
    temp=[]
    for file in os.listdir(os.path.join(audio_data_path,songlist)):
        id = int(file.split(".")[0])
        temp.append((id,))
    temp.sort(key=lambda x:x[0])
    if len(songs_ids[songlist])==len(temp):
        print("Songlist :",songlist)
        fl=0
        for x in range(len(songs_ids[songlist])):
            if songs_ids[songlist][x][0]!=temp[x][0]:
                print("Song id assertion error")
                print(temp)
                print("\n\n\n")
                print(songs_ids[songlist])
                fl=1
                break
        if not fl:
            print("Check passed!!")
            print("Printing songlist information: ",len(songs_ids[songlist]))
    else:
        print("Length are not equal!!!")
        print("songs_ids length: ",len(songs_ids[songlist]))
        print("temp length: ",len(temp))
annotation_dir= script_path+"/annotation/"
subjects = ["first","second","third"]
map_file = "songlist_id_map.txt"
map_=defaultdict(list)
for (id,song_name) in songs_ids["new_songs"]:
    map_["new_songs"].append((id,))
for line in open(os.path.join(annotation_dir,map_file)).readlines():
    if line.split()[0]=="cm_lb":
        key_="lb_songs"
    else:
        key_="5th_sem_songs"
    map_[key_].append((int(line.split()[1]),int(line.split()[2])))
for songlist in map_:
    map_[songlist].sort(key = lambda x:x[0])
#print(map_)
print("\n\n\nRe-performing the sanity checks...\n\n")
for songlist in map_:
    if len(map_[songlist])==len(songs_ids[songlist]):
        print("Songlist: ",songlist)
        fl=0
        for x in range(len(map_[songlist])):
            if map_[songlist][x][0]!=songs_ids[songlist][x][0]:
                print("Song id assertion error")
                print(map_[songlist])
                print("\n\n\n")
                print(songs_ids[songlist])
                fl=1
                break
        if not fl:
            print("Check passed!!")
            print("Printing songlist information: ",len(map_[songlist]))
    else:
        print("Lengths are not equal!!!")
        print("songs_ids length: ",len(songs_ids[songlist]))
        print("map_ length: ",len(map_[songlist]))
'''count=Counter()
for songlist in map_:
    if songlist!="new_songs":
        count+=Counter(x[0] for x in map_[songlist])
for id in count:
    if count[id]>1:
        print(id,count[id])'''
tag_map={
0:"funny",
1:"not-funny",
2:"other"
}
subjects_tag_id_map={}
for subject in subjects:
    tag_id_map=defaultdict(list)
    for file in os.listdir(os.path.join(annotation_dir,subject)):
        if "iaa" in file:
            if "_and_" in file:
                songlists=[file.split(subject+"_iaa_")[1].split("_and_")[0],file.split(subject+"_iaa_")[1].split("_and_")[1].split(".")[0]]
                lines = open(os.path.join(os.path.join(annotation_dir,subject),file)).readlines()
                for line in lines:
                    serial_num = int(line.split()[0])
                    tag = int(line.split()[1])
                    for songlist in songlists:
                        for x,y in zip(map_[songlist],songs_ids[songlist]):
                            if serial_num==x[1]:
                                assert x[0]==y[0]
                                tag_id_map[songlist].append((x[0],tag_map[tag],y[1]))
            else:
                songlist=file.split(subject+"_iaa_")[1].split(".")[0]
                lines = open(os.path.join(os.path.join(annotation_dir,subject),file)).readlines()
                for line in lines:
                    id_ = int(line.split()[0])
                    tag = int(line.split()[1])
                    for x,y in zip(map_[songlist],songs_ids[songlist]):
                        if id_==x[0]:
                            assert x[0]==y[0]
                            tag_id_map[songlist].append((x[0],tag_map[tag],y[1]))
    subjects_tag_id_map[subject]=tag_id_map
with open("subjects_tag_id_map.pickle","wb") as fl:
    pickle.dump(subjects_tag_id_map,fl)
