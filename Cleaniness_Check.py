# -*- coding: utf-8 -*-
"""
Created on Sat Oct  6 10:11:38 2018

@author: youko
"""

import pandas as pd
import numpy as np

'''this file is to check the data cleaniness
'''

myData=pd.read_csv('full_dataset.csv')
##scope check
##formatting all columns
myData.Movie_gross = myData.Movie_gross.str.extract('(\d+\.\d+)').astype(np.float64)
myData.Movie_runtime = myData.Movie_runtime.str.extract('(\d+)').astype(np.int)
myData.Movie_yr = myData.Movie_yr.str.extract('(\d+)').astype(np.int) 
myData.Movie_gross.replace(np.nan,0,inplace=True)
##get the description of all columns
colname=list(myData.columns.values)
#p=myData['acousticness'].describe()
#k=p.to_frame()
#m=myData['key'].describe()
#j['key']
#k.join(j)
def get_description(colname,myData):
    describe=[]
    for i in colname:
        describe.append(myData[i].describe())
    dfdes=describe[0].to_frame()
    length=len(describe)
    for j in range(1,length):
        new=describe[j].to_frame()
        dfdes=dfdes.join(new)
    return dfdes

description=get_description(colname,myData)
##remove useless columns
str_cols=['Track_name','Track_ID','Album_name','Album_ID','Movie_name','Movie_genre']

for t in str_cols:
    del description[t]

##get rate of narows rate
def scope_check(myData,colname,min_val,max_val):
    '''min_val is a dataframe storing all min values of each column
    max_val is a data frame storing all max values of each column
    '''
    ##define a set to put values that are out of range
    count=0
    for j in range(0,len(myData)):
        if myData[colname][j]<min_val or myData[colname][j]>max_val:
            count=count+1  
    rate=count/len(myData) 
            
    return rate

#t=pd.DataFrame(columns=colname)
#t=t.append(myData[3:4])
#t=t.append(myData[7:8])
##remove duplicated rows
#def get_duplicated_rate(df,colname):
   # '''this function is to check duplicated rows rate for a specific column
   # '''
    #new=df.drop_duplicates(colname)
    #rate=1-(len(new)/len(df))
    #return rate
numericcol = ['acousticness',
 'danceability',
 'duration_ms',
 'energy',
 'instrumentalness',
 'key',
 'liveness',
 'loudness',
 'mode',
 'speechiness',
 'tempo',
 'time_signature',
 'valence',
 'popularity',
 'Movie_gross',
 'Movie_rate',
 'Movie_runtime',
 'Movie_yr']
#columnname = ['acousticness',
##get the scope for each attribute
mindata = [0,0,0,0,0,0,0,-60,0,0,0,0,0,0,0.01,6.9,0,1900]
maxdata = [1,1,4000000,1,1,11,1,1,1,1,250,8,1,100,10000,10,1000,2018]
mindataframe = pd.DataFrame(data= [mindata], columns=numericcol)
maxdataframe = pd.DataFrame(data= [maxdata], columns=numericcol)
frames = [mindataframe, maxdataframe]
ScopeFrame = pd.concat(frames)
ScopeFrame=ScopeFrame.reset_index()
del ScopeFrame['index']
print(ScopeFrame)
##get narows rate
##get the scope for numeric columns
#scope_rate=[]
#duplicated_rate=[]
#for col in numericcol:
    #scope_rate.append(scope_check(myData,col,ScopeFrame[col][0],ScopeFrame[col][1]))
#outrange_rate=pd.DataFrame(data=[scope_rate],columns=numericcol)
##get the narows rate
null_rate = list(myData.isnull().sum()/len(myData))
na_rate=pd.DataFrame(data=[null_rate],columns=colname)
result_each_column=pd.DataFrame(columns=colname)

result=result_each_column.append(outrange_rate,sort=False)
result=result.append(na_rate)

##delete those movies that are out of range
myData=myData[myData['Movie_gross']!=0]
scope_rate=[]
for col in numericcol:
    scope_rate.append(scope_check(myData,col,ScopeFrame[col][0],ScopeFrame[col][1]))
outrange_rate=pd.DataFrame(data=[scope_rate],columns=numericcol)

null_rate = list(myData.isnull().sum()/len(myData))
na_rate=pd.DataFrame(data=[null_rate],columns=colname)
result_each_column=pd.DataFrame(columns=colname)

result=result_each_column.append(outrange_rate,sort=False)
result=result.append(na_rate)

filename='cleaned_data.csv'
myData.to_csv(filename, sep = ',',encoding='utf-8-sig', mode='a', index = False, float_format='%.8f')

resultfile='cleanness_result.csv'
result.to_csv(resultfile, sep = ',',encoding='utf-8-sig', mode='a', index = False, float_format='%.8f')

descriptionfile='description_attributes.csv'
description.to_csv(descriptionfile, sep = ',',encoding='utf-8-sig', mode='a', index =True, float_format='%.8f')

    

        
        