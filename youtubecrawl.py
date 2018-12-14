from __future__ import unicode_literals
import requests
import os
import codecs
import shutil
from bs4 import BeautifulSoup
import youtube_dl
import urllib3
from operator import itemgetter
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
#urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
#urllib3.disable_warnings()
script_path=os.path.dirname(os.path.realpath(__file__))
script_name="youtubecrawl.py"

"""Deinition of MyLogger class used by youtube-dl to print the message status"""

class MyLogger(object):
	"""docstring for MyLogger"""
	def debug(self, msg):
		pass
	def warning(self, msg):
		pass
	def error(self, msg):
		print(msg)

""" my_hook function returns the message when the status is finished"""

def my_hook(d):
	if d['status'] == 'finished':
		print('Done downloading, now converting ... ')

""" ydl_opts is the youtube-dl optional parameters, where we have specified the filetype and quality to be downloaded. In our case it's mp3 Audio file with a quality of 192"""

ydl_opts = {
	'format': 'bestaudio/best',
	'postprocessors': [{
		'key': 'FFmpegExtractAudio',
		'preferredcodec': 'mp3',
		'preferredquality': '192',
	}],
	'logger': MyLogger(),
	'progress_hooks': [my_hook],
}

""" Execution Script Starts !"""

print("Welcome to Automatic youtube !")
#user_choice = str(input("Enter the video you want to search for: "))
song_info=[]
#song_names_file_path="/home/priyansh/Downloads/honours_project/may_work/paclic/youtube_mp3_downloader/songs_list.txt"
#song_names_file_path="/home/priyansh/Downloads/honours_project/may_work/paclic/incomplete.txt"
song_names_file_path="/home/priyansh/Downloads/honours_project/may_work/paclic/songs_list2.txt"
with codecs.open(song_names_file_path,'r','utf-8') as fl:
	for line in fl:
		if line!="\n" and line!="":
			song_name = line.split('"')[1].rstrip()
			my_file_no = line.split('"')[0].rstrip().split(".")[0]
			song_info.append((song_name,int(my_file_no)))
fl.close()
song_info=sorted(song_info,key=itemgetter(1))
cnt=198
cnt1=cnt
#fd2=codecs.open("/home/priyansh/Downloads/honours_project/may_work/paclic/incomplete.txt",'w','utf-8')
for x in range(cnt1-1,len(song_info)):
	#if song_info[x][0]=="Sarkai Lo khatiya" or song_info[x][0]=="Tinku jiya":
	print(song_info[x][0])
	print(cnt)
	user_choice = song_info[x][0]+" song"
	user_choice = user_choice.lower()
	user_choice_list = user_choice.split()
	search_url = "https://www.youtube.com/results?search_query="
	search_url = search_url + user_choice_list[0]
	for i in range(1, len(user_choice_list)):
		search_url = search_url + "+" + user_choice_list[i]

	#print(search_url)
	page=requests.get(search_url, verify=False)
	#print(page)
	soup = BeautifulSoup(page.content, 'html.parser')
	#print(soup)
	results_list = soup.find_all(class_="yt-uix-tile-link")
	#print(results_list)
	views_list = soup.find_all(class_="yt-lockup-meta-info")
	#print(views_list)
	top_views_list = []
	for i in range(0,1):
		view = str(views_list[i].text)
		index = view.find("ago")
		final_view = view[index+3:len(view)-6]
		#print(final_view)
		final_view = final_view.split(",")
		final_view = "".join(final_view)
		try:
			int_final_view = int(final_view)
		except ValueError:
			continue
		top_views_list.append(int_final_view)

	maximum_views = max(top_views_list)
	max_views_index = top_views_list.index(maximum_views)
	link = results_list[max_views_index]['href']

	topmost_link = "https://youtube.com" + link
	try:
		page1 = requests.get(topmost_link, verify=False)
	except requests.exceptions.RequestException:
		#fd2.write(song_info[x][0]+"\n")
		cnt+=1
		continue

	soup1 = BeautifulSoup(page1.content, 'html.parser')
	video_title = soup1.find('span', class_="watch-title").text
	video_title = video_title.split()
	print("Title : " + ' '.join(video_title))
	video_author = soup1.find(class_="yt-user-info").text
	video_author = video_author.split()
	print("Author : " + ' '.join(video_author))
	video_views = soup1.find(class_="watch-view-count").text
	video_views = video_views.split()
	print("Views : " + ' '.join(video_views))
	video_date = soup1.find(class_="watch-time-text").text
	video_date = video_date.split()
	print("Date : " + ' '.join(video_date))
	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
		ydl.download([topmost_link])

	print("The video has been downloaded in mp3 format in your current directory !")
	for file in os.listdir(script_path):
		if os.path.isdir(script_path+"/"+file):
			continue
		else:
			if file!=script_name and file!="songs_list.txt":
				if "mp3" in file:
					new_name=str(song_info[x][1])+".mp3"
					os.rename(script_path+"/"+file,script_path+"/"+"audio_files/"+new_name)
			else:
				continue
	cnt+=1
#fd2.close()
