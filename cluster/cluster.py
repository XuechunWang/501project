#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 25 22:08:23 2018

@author: xuechunwang
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd

from sklearn.cluster import KMeans
from sklearn import preprocessing
import pylab as pl
from sklearn import decomposition
from pprint import pprint
from sklearn.metrics import silhouette_score,calinski_harabaz_score
from sklearn.preprocessing import normalize
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import DBSCAN

def data_processing():
    myData = pd.read_csv('full_dataset.csv', sep = ',',encoding = 'utf-8-sig')
    #myData = myData[:10000]
    # Just in case the data is not fully cleaned:
    myData.Movie_gross = myData.Movie_gross.str.extract('(\d+\.\d+)').astype(np.float64)
    myData.Movie_runtime = myData.Movie_runtime.str.extract('(\d+)').astype(np.int)
    myData.Movie_yr = myData.Movie_yr.str.extract('(\d+)').astype(np.int)
    myData.Movie_gross.replace(np.nan,0,inplace=True)
    #delete uesless varibales that are not used in the training model.
    del myData['Track_name']
    del myData['Track_ID']
    del myData['Album_name']
    del myData['Album_ID']
    del myData['Movie_name']
    del myData['Movie_genre']
    #myData.popularity.hist()
    #valueArray = myData.values
    myData= normalize(myData)
    return myData


def clustering(myData,method,name):	
    cluster_labels = method.fit_predict(myData)
    #Determine if the clustering is good
    #silhouette_avg = silhouette_score(myData, cluster_labels)
    calinski_avg = calinski_harabaz_score(myData, cluster_labels)
    print("The average calinski_harabaz_score is :", calinski_avg)  
    # using PCA
    pca2D = decomposition.PCA(2)
    # Turn the NY Times data into two columns with PCA
    plot_columns = pca2D.fit_transform(myData)
    # Plot using a scatter plot and shade by cluster label
    plt.scatter(x=plot_columns[:,0], y=plot_columns[:,1], c=cluster_labels)
    titlename = "Cluster Plot with " + name + " method"
    plt.title(titlename)
    #plt.savefig(titlename)
    plt.show()
    


def main():
    myData = data_processing()
    #initial the number of clusters 
    n = 6
    Hierarchical = AgglomerativeClustering(affinity = 'euclidean', compute_full_tree = 'auto',
                   connectivity = None, linkage = 'ward', memory = None, n_clusters=n,
                   pooling_func='deprecated')
    kmeans = KMeans(n_clusters = n)
    DbScan = DBSCAN(eps=0.3, min_samples=100)
    clustering(myData,kmeans,"K-means")
    clustering(myData,DbScan,"dbScane")
    clustering(myData,Hierarchical,"Hierarchical")
    

if __name__ == "__main__":
	main()