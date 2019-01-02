import os
from collections import Counter,defaultdict
import audiodiff as diff
import time
import cPickle as pickle
#script_path= os.path.dirname(os.path.abspath(__file__))
script_path = os.getcwd()
print script_path
print os.getcwd()
audio_dir=os.path.join(script_path,"trimmed_audio")
songlists=["funny","not_funny"]
all_songs=[]
for songlist in songlists:
    for audio_file in os.listdir(os.path.join(audio_dir,songlist)):
        all_songs.append(os.path.join(os.path.join(audio_dir,songlist),audio_file))

print len(all_songs)
cnt=0
l=len(all_songs)
temp={}

for s1 in all_songs:
    for s2 in all_songs:
        if s1!=s2:
        #print s1,s2
            temp[(s1,s2)]=diff.equal(s1,s2)
            cnt+=1
            #print diff.equal(s1,s2),cnt

out_path=os.path.join(script_path,"results")
if not os.path.exists(out_path):
    os.makedirs(out_path)
    
with open("results/duplicate_removal.pickle","wb") as fl:
    pickle.dump(temp,fl)
with open("results/duplicate_removal.pickle","rb") as fl:
    temp = pickle.load(fl)

for s1,s2 in temp:
    if temp[(s1,s2)]:
        print "{}, {}, {}, {}".format(s1.split("/")[-2],s2.split("/")[-2],s1,s2)