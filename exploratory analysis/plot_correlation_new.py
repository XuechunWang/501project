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
from mlxtend.preprocessing import TransactionEncoder
import matplotlib.pyplot as plt
from pandas.tools.plotting import scatter_matrix
from sklearn.preprocessing import normalize


#creat the plot of popularity, movie gross, energy
def hist_plot(myData,attributes):

    colors = ['#BFEFFF','#FFAEB9','#7CCD7C']
    for attribute, color in zip(attributes, colors):
        # zip() will truncate the longer arrays to match the length of the shorter array
        plt.figure()
        plt.hist(myData[attribute], alpha=0.6, color = color)
        titleLabel = "Histogram for "+ attribute
        plt.title(titleLabel)
        plt.show()

    # why necessary?
    plt.figure()
    plt.hist(myData.Movie_gross, range = (400,max(myData.Movie_gross)),alpha=0.6, color = '#836FFF')
    titleLabel = "Historgram for Movie Gross above 400?"
    plt.title(titleLabel)
    plt.show()
    #####

#The following function can creat a pair wised correlation between all numerical variables and write it to a text file        
def correlate(myData):
    # select only numeric columns
    numericDF = myData.select_dtypes(include = np.number)
    # normalize the data frame and 
    # make a correlation data frame for all the numeric variables
    corr_dataframe = pd.DataFrame(normalize(numericDF)).corr()
    # write to an output file
    with open('correlate.txt', 'w') as f:
        f.write(corr_dataframe.to_string())
    # create a scatter plot for all attributes
    all_attributes =numericDF.columns.get_values().tolist()
    filename = "all attributes scatter matrix.png"
    scatter_plot(numericDF,all_attributes,filename)
    # createa scatter plot for three selected attributes
    selected_attributes = ["popularity","Movie_gross","Movie_rate"]
    filename2 = "selected attributes scatter matrix.png"
    scatter_plot(numericDF,selected_attributes,filename2)

def scatter_plot(myData,attributes,filename):
    my_scatter = pd.plotting.scatter_matrix(
                                myData[attributes],
                                figsize = [40,40],
                                alpha = 0.4,
                                )
    for ax in my_scatter.ravel():
        ax.set_xlabel(ax.get_xlabel(), fontsize = 8, rotation = 0)
        ax.set_ylabel(ax.get_ylabel(), fontsize = 8, rotation = 90)
    plt.savefig(filename, dpi = 120)

    
def associationRule(myData):
    # select only the last six columns which are movie attributes
    # and drop duplicate rows
    movieData = myData.iloc[:,-6:].drop_duplicates()
    
    # remove space in each string and split the string by comma
    genreData = [genres.replace(" ","").split(",") for genres in movieData["Movie_genre"]]
   
    # use apriori package to return frequent itemsets
    # the following code is adapted from 
    # https://rasbt.github.io/mlxtend/user_guide/frequent_patterns/association_rules/
    # #example-1-generating-association-rules-from-frequent-itemsets
    te = TransactionEncoder()
    te_ary = te.fit(genreData).transform(genreData)
    df = pd.DataFrame(te_ary, columns=te.columns_)
    
    # use five different support levels

    min_supportList = [0.05,0.1,0.2,0.4,0.8]
    # reset pandas to display the whole table for association rules
    pd.set_option('max_columns',10)
    with open("assocication rule results.txt", "w") as f:
        for min_support in min_supportList:
            print("min_support =", min_support,file = f)
            print("",file = f )
            frequent_itemsets = apriori(df,min_support = min_support, use_colnames=True)
            
            # check if the frequent itemsets data frame is empty
            if frequent_itemsets.empty:
                print("The minimum support level is too high. "
                      "Frequent Itemsets is empty!", file = f)
            else: 
                print(frequent_itemsets,file = f)
                print("",file = f)
                
            # print association rules when min_support = 0.1 as an example
            if min_support == 0.1:
                print("Association Rules:", file = f)
                rules = association_rules(frequent_itemsets, metric="support", min_threshold=min_support)
                print(rules, file = f)
                print("",file = f)

def main():
    
    myData = pd.read_csv('cleaned_data.csv', sep=',',encoding='utf-8-sig')
    hist_plot(myData, ['popularity','Movie_gross','energy'])   
    associationRule(myData)
    correlate(myData)    


if __name__ == "__main__":
	main()