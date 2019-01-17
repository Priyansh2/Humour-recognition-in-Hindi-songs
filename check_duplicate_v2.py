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
temp1={}
temp2={}
temp3={}
for s1 in all_songs:
    for s2 in all_songs:
        if s1!=s2:
            temp1[(s1,s2)]=diff.equal(s1,s2)
            temp2[(s1,s2)]=diff.audio_equal(s1,s2)
            temp3[(s1,s2)]=diff.tags_equal(s1,s2)    
            cnt+=1
            
out_path=os.path.join(script_path,"results")
if not os.path.exists(out_path):
    os.makedirs(out_path)
    
with open("results/duplicate_temp1.pickle","wb") as fl:
    pickle.dump(temp1,fl)
with open("results/duplicate_temp1.pickle","rb") as fl:
    temp1 = pickle.load(fl)

with open("results/duplicate_temp2.pickle","wb") as fl:
    pickle.dump(temp2,fl)
with open("results/duplicate_temp2.pickle","rb") as fl:
    temp2 = pickle.load(fl)

with open("results/duplicate_temp3.pickle","wb") as fl:
    pickle.dump(temp3,fl)
with open("results/duplicate_temp3.pickle","rb") as fl:
    temp3 = pickle.load(fl)

print("Printing in format s1_dir,s2_dir,s1_path,s2_path\n")
for s1,s2 in temp1:
    if temp1[(s1,s2)]:
        print "{}, {}, {}, {}".format(s1.split("/")[-2],s2.split("/")[-2],s1,s2)
print("----------------------------------------------\n")
for s1,s2 in temp2:
    if temp2[(s1,s2)]:
        if temp2[(s1,s2)]!=temp1[(s1,s2)]:
            print "{}, {}, {}, {}".format(s1.split("/")[-2],s2.split("/")[-2],s1,s2)
#print("----------------------------------------------\n")        
#for s1,s2 in temp3:
    #if temp3[(s1,s2)]:
        #print "{}, {}, {}, {}".format(s1.split("/")[-2],s2.split("/")[-2],s1,s2)                