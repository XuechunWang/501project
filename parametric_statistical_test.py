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
from sklearn import linear_model
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm




#Read data and delete non_numerical varivales to prepare for t-test
def data_processing():
    myData = pd.read_csv('full_dataset.csv', sep = ',',encoding = 'utf-8-sig')
    # Just in case the data is not fully cleaned
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

def linear_reg(x,y):
    model = LinearRegression()
    
    regr = model.fit(x, y)
    RSquare = model.score(x, y)
    print('Intercept: \n', regr.intercept_)
    print('Coefficients: \n', regr.coef_)
    print('The coefficient of determination R^2 of the prediction: \n', RSquare)

def main():
    #Process the data
    normalizedData = data_processing()
    mode = normalizedData['mode']
    energy = normalizedData['energy']
    danceability = myData['danceability']
    mode_value = mode.values
    energy_value = energy.values
    danceability_value = danceability.values
    
    #T-test on two groups: mode&energy, mode&danceability
    ttest(mode_value,energy_value)
    ttest(mode_value,danceability_value)
    
    #Linear Regression on how popularity is related to valence, movie_gross, movie rate
    x, y = normalizedData[['valence','Movie_gross','Movie_rate']], normalizedData.popularity
    linear_reg(x,y)
    
if __name__ == "__main__":
    main()
    
    
    
    

    
    
    
    
