# -*- coding: utf-8 -*-
"""
Created on Sun Oct 28 21:40:54 2018

@author: Yuhui Tang
"""


# Import Libraries
import numpy as np
import pandas as pd
from scipy import stats
from scipy.stats import ttest_ind
from sklearn.preprocessing import normalize

#Read data and delete non_numerical varivales to prepare for t-test
def data_processing():
    myData = pd.read_csv('full_dataset.csv', sep = ',',encoding = 'utf-8-sig')
    # normalize the data for t-test
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
    #normalized dataframe except movie_yr
    myData.loc[:, myData.columns != 'Movie_yr'] = normalize(myData.loc[:, myData.columns != 'Movie_yr'])
    return myData

#conduct t test
def ttest(x, y):
    ttest = ttest_ind(x, y)
    print(ttest)

def main():
    normalizedData = data_processing()
    mode = normalizedData['mode']
    energy = normalizedData['energy']
    danceability = myData['danceability']
    mode_value = mode.values
    energy_value = energy.values
    danceability_value = danceability.values
    
    ttest(mode_value,energy_value)
    ttest(mode_value,danceability_value)


if __name__ == "__main__":
    
    main()
    
    
    
    

    
    
    
    
