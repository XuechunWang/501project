import sys
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
import pandas as pd
import numpy as np

client_credentials_manager = SpotifyClientCredentials(client_id='591ea7a366954772b6b64fba87ac0a14', client_secret='8050bf7b0ef94cc2b3cf6cbf12683f7a')
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
sp.trace = False
readlist = pd.read_csv('tracklist.csv', sep = ',', encoding ='latin1')
tracklist = readlist
#print(tracklist['Trackid'])

def getAnalysis(tracklist):
		track_id= tracklist['Trackid']
		sound_sets=["sound_feature_"+ str(i) for i in np.arange(len(track_id))]
		for i in np.arange(len(track_id)):
			tid=[track_id[i]]
			try:
				#use the api the get audio feature here, parameter is the track_id
				sp3 = sp.audio_features(tid)
				sound_sets[i]= pd.DataFrame(sp3)	
			except:
				print("audio features error")
				sound_sets[i]=pd.DataFrame([0])
		
		sound_features=pd.concat(sound_sets)
		sound_features["track_id"]=track_id.values
		return(sound_features)


def getPopularity(tracklist):
	track_id= tracklist['Trackid']
	columnname = ['popularity']
	populist = pd.DataFrame(columns = columnname)
	for i in np.arange(len(track_id)):
		tid=track_id[i]
		#print(tid)
		try:
			track_popu = sp.track(tid)['popularity']
			tempframe = pd.DataFrame([track_popu],columns = columnname)
			populist = populist.append(tempframe)
		except:
			populist = populist.append(None)
	return(populist)

populist = getPopularity(tracklist)

#fea=featurelist
#fea['popul'] = popu['popularity']
featurelist = getAnalysis(tracklist)
featurelist.loc[:,'popularity'] = populist['popularity'].tolist()
myFileName="featurelist.csv"
##write to txt files

#np.savetxt(r'featurelist.txt', featurelist.values, fmt='%d')
featurelist.to_csv(myFileName, sep = ',', mode='a', index = False, float_format='%.8f')
