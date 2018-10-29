#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 25 23:22:55 2018

@author: xuechunwang
"""
import numpy as np
import pandas as pd
from mlxtend.preprocessing import OnehotTransactions
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
import matplotlib.pyplot as plt
from pandas.tools.plotting import scatter_matrix

def association(movieData):
    newData = movieData.genres
    #newData =newData[:100]
    movie_genre_list = []
    #create a list of genre set of movies
    for genre in newData:
        genre_set = genre.split('|')
        movie_genre_list.append(genre_set)
    oht = OnehotTransactions()
    
    oht_ary = oht.fit(movie_genre_list).transform(movie_genre_list)
    #get the datafram of true and false table of movie genre
    Boolean_df = pd.DataFrame(oht_ary, columns=oht.columns_)
    #print (Boolean_df)           
    #Set the minimum of support rate to be 0.1
    frequent_itemsets = apriori(Boolean_df, min_support=0.1, use_colnames=True)
    print (frequent_itemsets)
     
    association_rules(frequent_itemsets, metric="confidence", min_threshold=0.7)
    rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1.2)
    print (rules)

#The following function can creat a pair wised correlation between all numerical variavles and write it to text file    
def correlation(myData):
    newData = myData
    #make sure the data is cleaned 
    del newData['Track_name']
    del newData['Track_ID']
    del newData['Album_name']
    del newData['Album_ID']
    del newData['Movie_name']
    del newData['Movie_genre']
    corr_dataframe = newData.corr()
    tfile = open('correlation.txt', 'a')
    tfile.write(corr_dataframe.to_string())
    tfile.close()
    

#creat the plot of popularity, movie gross, energy
def hist_plot(myData):
#    myData.Movie_gross = myData.Movie_gross.str.extract('(\d+\.\d+)').astype(np.float64)
#    myData.Movie_gross.replace(np.nan,0,inplace=True)
    plt.hist(myData.popularity, alpha=0.6, color = '#BFEFFF')
    titleLabel = "Historgram for Popularity"
    plt.title(titleLabel)
    plt.show()
    plt.clf()
    plt.hist(myData.Movie_gross, alpha=0.6, color = '#FFAEB9')
    titleLabel = "Historgram for Movie Gross"
    plt.title(titleLabel)
    plt.show()
    plt.clf()
    plt.hist(myData.Movie_gross, range = (400,max(myData.Movie_gross)),alpha=0.6, color = '#836FFF')
    titleLabel = "Historgram for Movie Gross"
    plt.title(titleLabel)
    plt.show()
    plt.clf()
    plt.hist(myData.energy, alpha=0.6, color = '#7CCD7C')
    titleLabel = "Historgram for Track Energy"
    plt.title(titleLabel)
    plt.show()

def scatter_plot(myData):
    newData = myData[['Movie_gross','popularity','energy']]
    scatter_matrix(newData)
    plt.show()

def main():
    movieData = pd.read_csv('movie_metadata.csv', sep=',',encoding='utf-8-sig')
    myData = pd.read_csv('full_dataset.csv', sep=',',encoding='utf-8-sig')
    myData.Movie_gross = myData.Movie_gross.str.extract('(\d+\.\d+)').astype(np.float64)
    myData.Movie_runtime = myData.Movie_runtime.str.extract('(\d+)').astype(np.int)
    myData.Movie_yr = myData.Movie_yr.str.extract('(\d+)').astype(np.int)
    myData.Movie_gross.replace(np.nan,0,inplace=True)
    correlation(myData)
    hist_plot(myData)
    scatter_plot(myData)
    association(movieData)
    
if __name__ == "__main__":
	main()