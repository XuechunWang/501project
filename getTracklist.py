##read from movie list, search for album and inside tracks. Then creat a new csv file for combined data.
import sys
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
import json
import spotipy.util as util
import pandas as pd

client_credentials_manager = SpotifyClientCredentials(client_id='d386e5bb6d044d4d8cb34e60b526af77', client_secret='1c2e64717fb04fbb9bbda7912e667be4')
sp = sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
sp.trace = False

filmData = pd.read_csv('cleanMVData.csv', sep = ',', encoding ='latin1')
#filmData=filmData['cleanTitleSpot']
columnname = ['Trackname','Trackid','Albumname','Albumid','Moviename',
                'Moviegenre','Moviegross','Movierate','Movieruntime','Movievote','Movieyr']
trackData = pd.DataFrame(columns=columnname)
# find album by name

    # #print(filmData)[10:]
#filmData=filmData[:20]
for i in range(0, len(filmData)):
    moviename = filmData.iloc[i]['cleanTitleSpot']
    moviegenre = filmData.iloc[i]['genre']
    moviegross = filmData.iloc[i]['gross']
    movierate = filmData.iloc[i]['rate']
    movieruntime = filmData.iloc[i]['runtime']
    movievote= filmData.iloc[i]['vote']
    movieyr = filmData.iloc[i]['yr']
    results = sp.search(q = "album:" + moviename, type = "album")
    #print(results)
    #get the first album uri
    if results['albums']['total'] != 0:
        albumid = results['albums']['items'][0]['uri']
        albumname = results['albums']['items'][0]['name']
        #get album tracks
        tracks = sp.album_tracks(albumid)
        for track in tracks['items']:
            trackid = track['id']
            trackname = track['name']
            newTrack = pd.DataFrame([[trackname,trackid,albumname,albumid,moviename,
                moviegenre,moviegross,movierate,movieruntime,movierate, movieyr]],columns=columnname)
            trackData = trackData.append(newTrack)

#print(trackData)
myFileName="tracklist.csv"
trackData.to_csv(myFileName, sep = ',', mode='a', index = False, float_format='%.8f')