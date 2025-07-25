# -*- coding: utf-8 -*-
"""
Created on Fri Jul 25 11:10:43 2025

@author: charl
"""

    
from pathlib import Path
#%% This snippet wipes the subsidiary folders- may be usefful, but might not be
import shutil
folders=[r"C:\Users\charl\OneDrive\Documents\CU lyrics\CU-Lyrics\Welsh songs",r"C:\Users\charl\OneDrive\Documents\CU lyrics\CU-Lyrics\English songs",r"C:\Users\charl\OneDrive\Documents\CU lyrics\CU-Lyrics\Bilingual songs"]
for folder in folders:
    folder_path = Path(folder)

    for item in folder_path.iterdir():
        if item.is_file() or item.is_symlink():
            item.unlink()  # Remove file or symbolic link
        elif item.is_dir():
            shutil.rmtree(item)  # Remove directory
#%%

raw_song_paths=[]
folder_path = Path(r"C:\Users\charl\OneDrive\Documents\CU lyrics\CU-Lyrics\Songs")
for file in folder_path.iterdir():
    if file.is_file():  # Check if it's a file
        raw_song_paths.append(file)
        
for song_path in raw_song_paths:
    with open(song_path,"r") as song:
        print()
        
#%%        
        


