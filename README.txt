#501 Project
#by Xunchun Wang, Yao Huang, Yuhui Tang and Yan Liu
#Github: https://github.com/XuechunWang/501project/

## Acquire Movies' Data from IMDb
IMDB.py: a web scraper to acquire movie data from IMDb's advanced search web page.
The output file is mv.csv.
mv.csv: contains (uncleaned) general data, such as gross, votes, of all the filtered 2122 movies.
 
cleanMVTitle.py : reads in mv.csv, fixes scrape errors, cleans titles and adds two new columns to mv.csv, one column of cleaned movie titles and the other specifically for query in Spotify. The output file is cleanMVData.csv.
cleanMVData.csv: contains cleaned movie data.

Before and After Cleaning Titles.py: a test code used to check the number of failed movies (no soundtracks in Spotify) before and after cleaning movie titles. It has two output files: noTrackMV(Original Title).csv and noTrackMV(Clean Title).csv
noTrackMV(Original Title).csv: lists failed movies when using original titles.
noTrackMV(Clean Title).csv: lists failed movies when using cleaned titles.

##Acquire Soundtracks' Data from Spotify
getTracklist.py: uses the movie title in cleanMVData.csv as input to find the corresponding soundtrack albums and the track id of each track in every album. The output file is tracklist.csv.
tracklist.csv: includes soundtrack albums, track ids and movies' data. 
getFeaturelist.py: uses the track ids in tracklist.csv as input to scrape feature data, such as acousticness index, danceability index, duration of the soundtrack, of each soundtrack. The output file is featurelist.csv. 
featurelist.csv: includes desired musical features and popularity of all the soundtracks.

##Quality Check and Data Merging
Feature_Movie_Clean.py: reads in the two raw datasets, tracklist.csv and featurelist.csv, and cleans them. It also checks the scope and null values to prepare for merging. The output files are track_quality.csv, feature_quality.csv and full_dataset.csv.
track_quality.csv: includes out-of-range-rate and null value rate for data in tracklist.csv.
feature_quality.csv: includes null value rate for data in featurelist.csv. (out-of-rage rate will be computed later after merging)
full_dataset.csv: an aggregate data file of tracklist.csv and featurelist.csv, eliminated duplicate rows. It includes all the general data of movies and musical features of soundtracks.

##Data Cleaning 
Cleanliness_Check.py: reads in the full_dataset.csv, formats certain columns into the desired data type, checks the scope of each attribute and describe the data. It has three output files: cleaned_data.csv, cleanness_result.csv, description_attributes.csv.
description_attributes.csv: describes each attribute using count, mean, min, max etc.
cleanness_result.csv: includes all the attributes, their out-of-range rate (the first row) and their null value rate (the second row).
cleaned_data.csv: includes all the cleaned data.


