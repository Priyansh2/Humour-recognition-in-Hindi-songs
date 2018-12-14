from __future__ import unicode_literals
import os
import youtube_dl
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}
path1="/home/priyansh/Downloads/honours_project/incomplete3.txt"
#path2="/home/priyansh/Downloads/honours_project/incomplete2.txt"
url1=[]
#url2=[]
with open(path1,'r') as f1:
    for line in f1:
        url1.append((line.split('"')[0].rstrip(),line.split('"')[1].rstrip(),line.split('"')[2].rstrip()))
#with open(path2,'r') as f2:
    #for line in f2:
        #url2.append((line.split('"')[0].rstrip(),line.split('"')[1].rstrip(),line.split('"')[2].rstrip()))


o1="/home/priyansh/Downloads/honours_project/audio_extract/a1/"
o2="/home/priyansh/Downloads/honours_project/audio_extract/a2/"
main_path="/home/priyansh/Downloads/honours_project/audio_extract"
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    for url in url1:
        ydl.download([url[2]])
        for file in os.listdir(main_path):
    		if os.path.isdir(main_path+"/"+file):
    			continue
    		else:
    			if "mp3" in file:
    				new_name=url[0]+".mp3"
    				os.rename(main_path+"/"+file,main_path+"/"+"a1/"+new_name)
    			else:
    				continue
    '''for url in url2:
        ydl.download([url[2]])
        for file in os.listdir(main_path):
    		if os.path.isdir(main_path+"/"+file):
    			continue
    		else:
    			if "mp3" in file:
    				new_name=url[0]+".mp3"
    				os.rename(main_path+"/"+file,main_path+"/"+"a2/"+new_name)
    			else:
    				continue'''
