import sys
import spotipy

from spotipy.oauth2 import SpotifyClientCredentials

import os
import json
import spotipy.util as util
import pandas as pd
import time

client_credentials_manager = SpotifyClientCredentials(client_id='d386e5bb6d044d4d8cb34e60b526af77', client_secret='1c2e64717fb04fbb9bbda7912e667be4')
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
sp.trace = False


filmData = pd.read_csv('cleanMVData.csv', sep = ',', encoding ='utf-8')
titleColumns = ['title','cleanTitleSpot']
noTrackMV = [[],[]]
n = 0 # represents the two columns' index
 
for titleColumn in titleColumns:
    count = 0 # count number of tracks acquired
    for movie in filmData[titleColumn]:
        #time.sleep(2)
        results = sp.search(q = "album:" + movie, type = "album")
        if results['albums']['total'] != 0:
            albumid = results['albums']['items'][0]['uri']
            tracks = sp.album_tracks(albumid)
            number = len(tracks['items'])
            count += number
        else:
            print("Still no tracks: ", movie)
            noTrackMV[n].append(movie)
    print('Using ' + titleColumn)    
    print("Total number of movie with tracks:")
    print(len(filmData[titleColumn]) - len(noTrackMV[n]))  # total movies minus none  
    print("Total number of movie still with no tracks:")
    print(len(noTrackMV[n]))
    print("Total number of tracks acquired:")
    print(count)
    n += 1

    
noTrackMVDF1 = pd.DataFrame({'No Track MV (Original Title)': noTrackMV[0]})
noTrackMVDF2 = pd.DataFrame({'No Track MV (Clean Title)': noTrackMV[1]})

with open("noTrackMV(Original Title).csv", 'w', encoding = 'utf-8') as f:
    noTrackMVDF1.to_csv(f, sep = ',', index = True)
    
with open("noTrackMV(Clean Title).csv", 'w', encoding = 'utf-8') as f:
    noTrackMVDF2.to_csv(f, sep = ',', index = True)   
