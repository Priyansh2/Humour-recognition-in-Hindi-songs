import os
#path1="/media/priyansh/SUMMER/UBUNTU_DOCUMENTS/backup_all_songs/non_code_mixed/"
#path2="/media/priyansh/SUMMER/UBUNTU_DOCUMENTS/backup_all_songs/code_mixed/out2_cm/"
#path3="/media/priyansh/SUMMER/UBUNTU_DOCUMENTS/backup_all_songs/code_mixed/lyrics_bogie_cm/"
output_path="/media/priyansh/SUMMER/UBUNTU_DOCUMENTS/trimmed_audio/new_songs/"
#non_code_mixed_songs_path="/media/priyansh/SUMMER/UBUNTU_DOCUMENTS/trimmed_audio/non_code_mixed/"
#out2_cm_songs_path="/media/priyansh/SUMMER/UBUNTU_DOCUMENTS/trimmed_audio/code_mixed/out2_cm/"
#lyrics_bogie_cm_songs_path="/media/priyansh/SUMMER/UBUNTU_DOCUMENTS/trimmed_audio/code_mixed/lyrics_bogie_cm/"
path1="/home/priyansh/Downloads/honours_project/may_work/paclic/youtube_mp3_downloader/audio_files/"
all_files=[]
paths=[]
paths.append(path1)
#paths.append(path2)
#paths.append(path3)
for path in paths:
    if path==path1:
        for files in os.listdir(path):
            old_file_path=path+files
            #new_file_path=non_code_mixed_songs_path+files
            new_file_path=output_path+files
            cmd="ffmpeg -t 60 -i "+old_file_path+" -acodec copy "+new_file_path
            os.system(cmd)
            #cnt+=1
    '''else:
        if path==path2:
            for files in os.listdir(path):
                old_file_path=path+files
                new_file_path=out2_cm_songs_path+files
                cmd="ffmpeg -t 60 -i "+old_file_path+" -acodec copy "+new_file_path
                os.system(cmd)
        else:
            for files in os.listdir(path):
                old_file_path=path+files
                new_file_path=lyrics_bogie_cm_songs_path+files
                cmd="ffmpeg -t 60 -i "+old_file_path+" -acodec copy "+new_file_path
                os.system(cmd)'''
