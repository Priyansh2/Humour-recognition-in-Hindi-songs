#!/usr/bin/env python
#!-*- coding: utf-8 -*-
import os
import codecs
import shutil
from statsmodels.stats import inter_rater
from nltk import agreement
from sklearn.metrics import cohen_kappa_score
from collections import defaultdict
from collections import Counter
file1="/home/priyansh/Downloads/honours_project/may_work/paclic/code_files/file_iaa.txt"
file2="/home/priyansh/Downloads/honours_project/may_work/paclic/code_files/IAA/file_iaa.txt"
file3="/home/priyansh/Downloads/honours_project/may_work/paclic/code_files/third_annotation/file_iaa.txt"
map_file="/home/priyansh/Downloads/honours_project/may_work/paclic/code_files/mod_all_files.txt"
rater1=[]
rater2=[]
rater3=[]
files=[]
files.append(file1)
files.append(file2)
files.append(file3)
extra_files=[]
extra_files.append("/home/priyansh/Downloads/honours_project/may_work/paclic/code_files/new_songs_annotation/1_file_iaa.txt")
extra_files.append("/home/priyansh/Downloads/honours_project/may_work/paclic/code_files/new_songs_annotation/2_file_iaa.txt")
extra_files.append("/home/priyansh/Downloads/honours_project/may_work/paclic/code_files/new_songs_annotation/3_file_iaa.txt")
all_files=[]
duplicate_songs_list="/home/priyansh/Downloads/honours_project/may_work/paclic/code_files/dup.txt"
dup_songs=[]
with codecs.open(duplicate_songs_list,'r','utf-8') as fl:
    for line in fl:
        dup_songs.append((line.split()[0],line.split()[1]))

fl.close()

fd=codecs.open(map_file,'w','utf-8')
filtered_files=[]
g2=[]
bl=[]
T=0
g1=[]
orig_map_file="/home/priyansh/Downloads/honours_project/may_work/paclic/code_files/all_files.txt"
with codecs.open(orig_map_file,'r','utf-8') as fl:
    for line in fl:
        if line!="\n" and line!="":
            temp = line.split()
            if (temp[0],temp[1]) not in dup_songs:
                if temp[0]=="non_cm":
                    #g1.append(temp[1])
                    T+=1
                    g2.append(temp[2])
                g1.append((temp[0],temp[2]))
                #T+=1
                fd.write(temp[0]+"\t\t\t\t\t"+temp[1]+"\t\t\t\t\t"+temp[2]+"\n")
fl.close()
fd.close()
#print len(g1)-len(g2)
def search(sng):
    for x in range(0,len(g1)):
        element = g1[x][1]
        tag=g1[x][0]
        if element==sng:
            if tag!="non_cm":
                return 1
            else:
                return 0
    return 0

def find_ratings(file,flag):
    ratings=[]
    with codecs.open(file,'r','utf-8') as fl:
        for line in fl:
            if line!="\n" and line!="":
                if flag==0:
                    flg=0
                    for sng in bl:
                        if sng[2]==line.split()[0]:
                            flg=1
                            break
                    if flg==1:
                        ratings.append(int(line.split()[1]))
                    else:
                        if search(line.split()[0])==1:
                            ratings.append(int(line.split()[1]))
                else:
                    if line.split()[0] in g2:
                        ratings.append(int(line.split()[1]))
                #ratings.append(int(line.split()[1]))
    fl.close()
    return ratings

def embedding_more_ratings(extra_files,ratings):
    fg=0
    cnt=0
    #L=0
    for x in range(0,len(extra_files)):
        with codecs.open(extra_files[x],'r','utf-8') as fl:
            for line in fl:
                if line!="\n" and line!="":
                    #print ratings[x]
                    ratings[x].append(int(line.split()[1]))
                    if fg==0:
                        #L+=1
                        all_files.append(("true_cm_lb",line.split()[0]))
                        cnt+=1
        fl.close()
        if cnt==150:
            #print "yes"
            fg=1
            cnt=0
    #print L
    #print len(all_files)
    return ratings

def Final_extraction(data):

    print "Data extraction is in progress...."
    cnt=1
    for dat in data:
        if dat[1]=="fun":
            data_path="/home/priyansh/Downloads/honours_project/may_work/paclic/code_files/final_data/funny/"
        else:
            data_path="/home/priyansh/Downloads/honours_project/may_work/paclic/code_files/final_data/not_funny/"
        songs=dat[0]
        for sng in songs:
            if sng[0]=="cm_lb" or sng[0]=="true_cm_lb":
                corpus_path="/home/priyansh/Downloads/honours_project/may_work/paclic/code_files/sota_transliterated/"
                #shutil.copy(corpus_path+sng[1],data_path+str(cnt)+".txt")
            elif sng[0]=="cm_out2":
                corpus_path="/home/priyansh/Downloads/honours_project/may_work/paclic/final_dataset/code_mixed/main_code_mix/"

            else:
                corpus_path="/home/priyansh/Downloads/honours_project/may_work/paclic/final_dataset/non-code_mixed/"

            shutil.copy(corpus_path+sng[1]+".txt",data_path+str(cnt)+".txt")
            cnt+=1
    print "Data extraction process completed!!!"


def filtering(funny_songs):
    for song in funny_songs:
        filtered_files.append(song)

    for x in range(0,len(filtered_files)):
        with codecs.open(map_file,'r','utf-8') as fl:
            for line in fl:
                if line!="\n" and line!="":
                    tmp=line.split()
                    if filtered_files[x]==(tmp[0],tmp[1]):
                        bl.append((tmp[0],tmp[1],tmp[2]))
        fl.close()
    #print len(filtered_files)
    all_files[:]=[]
    compute_kappa(files,0)



def extract_final_data(ratings,flag):
    reject_songs=[]
    funny_songs=[]
    not_funny_songs=[]
    with codecs.open(map_file,'r','utf-8') as fl:
        for line in fl:
            if line!="\n" and line!="":
                temp=line.split()
                if flag==0:
                    if temp[0]=="non_cm":
                        if (temp[0],temp[1],temp[2]) in bl:
                            all_files.append((temp[0],temp[1]))
                    else:
                        all_files.append((temp[0],temp[1]))
                else:
                    if temp[2] in g2:
                        all_files.append((temp[0],temp[1]))
                #all_files.append((temp[0],temp[1]))
    fl.close()
    for x in range(0,len(ratings[0])):
        L=[ratings[0][x],ratings[1][x],ratings[2][x]]
        if not [item for item, count in Counter(L).items() if count >1]:
            reject_songs.append((all_files[x][0],all_files[x][1]))
        else:
            d=defaultdict(int)
            for i in L:
                d[i]+=1
            result = max(d.iteritems(),key=lambda y:y[1])
            final_label=int(result[0])
            if final_label==0:
                funny_songs.append((all_files[x][0],all_files[x][1]))
            elif final_label==1:
                #print all_files[x]
                not_funny_songs.append((all_files[x][0],all_files[x][1]))
            else:
                reject_songs.append((all_files[x][0],all_files[x][1]))

    if len(ratings[0])==len(ratings[1])==len(ratings[2])==len(all_files):
        if len(funny_songs)+len(not_funny_songs)+len(reject_songs)==len(ratings[0]):
            print "Passed!!!"
        else:
            print "lol1"
    else:
        print "lol2"

    data=[]
    data.append((funny_songs,'fun'))
    data.append((not_funny_songs,'!fun'))
    print "Finally selected Total songs: "+str(len(data[0][0])+len(data[1][0]))
    print "Finally selected Total funny songs: "+str(len(data[0][0]))
    print "Finally selected Total not_funny songs: "+str(len(data[1][0]))

    if flag==0:
        Final_extraction(data)
    #Final_extraction(data)
    else:
        filtering(funny_songs)



def compute_kappa(files,flag):
   # all_files=[]
    for file in files:
        rater=find_ratings(file,flag)
        if file==file1:
            rater1=rater
        elif file==file2:
            rater2=rater
        else:
            rater3=rater
    #print len(rater1)
    #print len(rater2)
    #print len(rater3)
    ratings=[]
    ratings.append(rater1)
    ratings.append(rater2)
    ratings.append(rater3)
    if flag==0:
        ratings=embedding_more_ratings(extra_files,ratings)
    #embedding_more_ratings(extra_files,ratings)
    #print len(ratings[0])
    inp_mat=[]
    if len(ratings[0])==len(ratings[1])==len(ratings[2]):
        print "okay!!!"
        #for x in range(0,len(ratings)):
        for i in range(0,len(ratings[0])):
            temp=[ratings[0][i],ratings[1][i],ratings[2][i]]
            freq={y:temp.count(y) for y in temp}
            mat=[0,0,0]
            for cat,cat_freq in freq.iteritems():
                if cat==0:
                    mat[0]=int(cat_freq)
                elif cat==1:
                    mat[1]=int(cat_freq)
                elif cat==2:
                    mat[2]=int(cat_freq)
            inp_mat.append(mat)
    #print inp_mat
    #print fleissKappa(inp_mat,3)
    print "Cohen's kappa between rater1 and rater2: "+str(cohen_kappa_score(ratings[0],ratings[1]))
    print "Cohen's kappa between rater2 and rater3: "+str(cohen_kappa_score(ratings[1],ratings[2]))
    print "Cohen's kappa between rater1 and rater3: "+str(cohen_kappa_score(ratings[2],ratings[0]))
    print "Fliess Kappa: "+str(inter_rater.fleiss_kappa(inp_mat))
    extract_final_data(ratings,flag)


compute_kappa(files,1)








