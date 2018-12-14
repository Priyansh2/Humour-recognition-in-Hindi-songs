import os
from collections import Counter,defaultdict
import audiodiff as diff
import time
script_path= os.path.dirname(os.path.abspath(__file__))
audio_dir=os.path.join(script_path,"trimmed_audio")
songlists=["lb_songs","5th_sem_songs","new_songs"]
all_songs=[]
for songlist in songlists:
    for audio_file in os.listdir(os.path.join(audio_dir,songlist)):
        all_songs.append(os.path.join(os.path.join(audio_dir,songlist),audio_file))

print(len(all_songs))
cnt=0
l=len(all_songs)
temp={}
for s1 in all_songs:
    for s2 in all_songs:
        if s1!=s2:
            temp[(s1,s2)]=diff.equal(s1,s2)
            cnt+=1
            print(diff.equal(s1,s2),cnt)
for s1,s2 in temp:
    if temp[(s1,s2)]:
        print "{}{}{}{}".format(s1.split("/")[-2],s2.split("/")[-2],s1,s2)
'''dup_status={}
for songlist in songlists:
    dup_status[songlist]=defaultdict()
    for s1 in os.listdir(os.path.join(audio_dir,songlist)):
        for s2 in os.listdir(os.path.join(audio_dir,songlist)):
            if s1!=s2:
                dup_status[songlist][(s1,s2)]=diff.equal(os.path.join(os.path.join(audio_dir,songlist),s1),os.path.join(os.path.join(audio_dir,songlist),s2))
'''
'''for songlist in dup_status:
    print("Songlist: ",songlist)
    for s1,s2 in dup_status[songlist]:
        if dup_status[songlist][(s1,s2)]:
            print '{}{}'.format(s1,s2)'''
