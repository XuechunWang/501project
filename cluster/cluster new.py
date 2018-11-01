#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 25 22:08:23 2018

@author: xuechunwang Yan Liu
"""

import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd

from sklearn.cluster import KMeans
from sklearn import preprocessing
import pylab as pl
from pprint import pprint
from sklearn.metrics import silhouette_score,calinski_harabaz_score
from sklearn.preprocessing import normalize
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import DBSCAN
from mpl_toolkits.mplot3d import Axes3D
from sklearn.decomposition import PCA

def data_processing():
    myData = pd.read_csv('cleaned_data.csv', sep = ',',encoding = 'utf-8-sig')
    #delete uesless varibales that are not used in the training model.
    del myData['Track_name']
    del myData['Track_ID']
    del myData['Album_name']
    del myData['Album_ID']
    del myData['Movie_name']
    del myData['Movie_genre']
    #normalize data
    myData= normalize(myData)
    return myData


def clustering(myData,method,name):	
    cluster_labels = method.fit_predict(myData)
    #Determine if the clustering is good
    #silhouette_avg = silhouette_score(myData, cluster_labels)
    calinski_avg = calinski_harabaz_score(myData, cluster_labels)
    print("The average calinski_harabaz_score is :", calinski_avg)  
    # Use PCA
    # Turn the data into two columns with PCA
    plot_columns = PCA(n_components=2).fit_transform(myData)
    # Plot using a scatter plot and shade by cluster label
    plt.figure()
    plt.scatter(x=plot_columns[:,0], y=plot_columns[:,1], c=cluster_labels)
    titlename = "Cluster Plot with " + name + " method"
    plt.title(titlename)
    plt.savefig(titlename)
    plt.show()
    
    # plot a 3D graph for better visualization
    # the code is adapted from 
    # http://scikit-learn.org/stable/auto_examples/datasets/plot_iris_dataset.html
    # #sphx-glr-auto-examples-datasets-plot-iris-dataset-py
    fig = plt.figure(figsize=(8, 6))
    ax = Axes3D(fig, elev=-150, azim=110)
    X_reduced = PCA(n_components=3).fit_transform(myData)
    ax.scatter(X_reduced[:, 0], X_reduced[:, 1], X_reduced[:, 2], c=cluster_labels,
           cmap=plt.cm.Set1, edgecolor='k', s=40)    
    titlename2 = "First three PCA directions - "+ name
    ax.set_title(titlename2)
    ax.set_xlabel("1st eigenvector")
    ax.w_xaxis.set_ticklabels([])
    ax.set_ylabel("2nd eigenvector")
    ax.w_yaxis.set_ticklabels([])
    ax.set_zlabel("3rd eigenvector")
    ax.w_zaxis.set_ticklabels([])
    plt.savefig(titlename2)
    plt.show()
    


def main():
    myData = data_processing()
    #initial the number of clusters as 6
    n = 6
    Hierarchical = AgglomerativeClustering(affinity = 'euclidean', compute_full_tree = 'auto',
                   connectivity = None, linkage = 'ward', memory = None, n_clusters=n,
                   pooling_func='deprecated')
    kmeans = KMeans(n_clusters = n)
    DbScan = DBSCAN(eps=0.3, min_samples=100)
    clustering(myData,kmeans,"K-means")
    clustering(myData,DbScan,"DBScan")
    clustering(myData,Hierarchical,"Hierarchical")

if __name__ == "__main__":
	main()