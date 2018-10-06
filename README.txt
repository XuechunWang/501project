## Acquire Movies' Data from IMDb
IMDB.py: a web scraper to acquire movie data from IMDb's advanced search web page.
The output file is mv.csv.
mv.csv: contains (uncleaned) general data, such as gross, votes, of all the filtered 2122 movies.
 
cleanMVTitle.py : reads in mv.csv, fixes scrape errors, cleans titles and adds two new columns to mv.csv, one column of cleaned movie titles and the other specifically for query in Spotify. The output file is cleanMVData.csv.
cleanMVData.csv: contains cleaned general movie data.

Before and After Cleaning Titles.py: a test code used to check the number of failed movies (no soundtracks) before and after cleaning movie titles. It has two output files: noTrackMV(Original Title).csv and noTrackMV(Clean Title).csv
noTrackMV(Original Title).csv:  lists failed movies when using original titles.
noTrackMV(Clean Title).csv:  lists failed movies when using cleaned titles.

##Acquire Soundtracks' Data from Spotify
getFeaturelist.py: use the movie title as input to find the corresponding soundtrack albums and the track id of each track in every album. The output file is tracklist.csv.
tracklist.csv: includes movies' data, soundtrack albums and track ids.
getTracklist.py: use the track ids in tracklist.csv as input to scrape feature data, such as acousticness index, danceability index, duration of the soundtrack, of each soundtrack. The output file is sound_features.csv. 
sound_features.csv: includes 14 musical features and popularity of all the soundtracks.

## Full Data Sets
full_data.csv: an aggregate data file of mv.csv, tracklist.csv and sound_features.csv, includes all the general data of movies and musicial features of soundtracks.

## Data Cleaning 


