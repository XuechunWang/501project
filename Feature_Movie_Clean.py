# -*- coding: utf-8 -*-
"""
Created on Thu Oct  4 10:26:18 2018

@author: youko
"""
import pandas as pd
import numpy as np
##this .py file is used for cleaning the scraped raw data
##read the files
titles=pd.read_csv('tracklist.csv',sep=',',encoding='utf-8-sig')
titles.Moviegross = titles.Moviegross.str.extract('(\d+\.\d+)').astype(np.float64)
titles.Movieruntime = titles.Movieruntime.str.extract('(\d+)').astype(np.int)
#myData.Movie_gross.replace(np.nan,0,inplace=True)
##check its cleanness
title_colname=list(titles.columns.values)
title_null_rate = list(titles.isnull().sum()/len(titles))
title_na_rate=pd.DataFrame(data=[title_null_rate],columns=title_colname)

##title scope check
numeric_title_col=['Moviegross','Movierate','Movieruntime','Movievote']
title_outscope=[]

mindata = [0,6.9,0,6.9]
maxdata = [4000000,10,10000,10]
mindataframe = pd.DataFrame(data= [mindata], columns=numeric_title_col)
maxdataframe = pd.DataFrame(data= [maxdata], columns=numeric_title_col)
frames = [mindataframe, maxdataframe]
ScopeFrame = pd.concat(frames)
ScopeFrame=ScopeFrame.reset_index()
del ScopeFrame['index']
#print(ScopeFrame)
title_outscope=[]
for col in numeric_title_col:
    title_outscope.append(scope_check(titles,col,ScopeFrame[col][0],ScopeFrame[col][1]))
title_outrange_rate=pd.DataFrame(data=[title_outscope],columns=numeric_title_col)

title_quality=pd.DataFrame(columns=title_colname)
title_quality=title_quality.append(title_outrange_rate,sort=False)
title_quality=title_quality.append(title_na_rate)

##reset index 
feature=pd.read_csv('featurelist.csv',sep=',',encoding='utf-8-sig')
feature=feature.drop(columns=['0'])

del feature['analysis_url']
del feature['id']
del feature['track_href']
del feature['type']
del feature['uri']
del feature['track_id']

feature_col=list(feature.columns.values)
feature_null_rate = list(feature.isnull().sum()/len(feature))
feature_na_rate=pd.DataFrame(data=[feature_null_rate],columns=feature_col)

#feature_outscope=[]
#for col in feature_col:
    #feature_outscope.append(scope_check(feature,col,ScopeFrame[col][0],ScopeFrame[col][1]))
#feature_outrange_rate=pd.DataFrame(data=[feature_outscope],columns=feature_col)

feature_quality=pd.DataFrame(columns=feature_col)

feature_quality=feature_quality.append(feature_na_rate,sort=False)

##get the outputs
featurequalityfile='feature_quality.csv'
feature_quality.to_csv(featurequalityfile, sep = ',',encoding='utf-8-sig', mode='a', index = False, float_format='%.8f')

trackqualityfile='track_quality.csv'
title_quality.to_csv(trackqualityfile, sep = ',',encoding='utf-8-sig', mode='a', index = False, float_format='%.8f')

#def drop_unmatched(row,col1,col2):
   # if row[col1] != row[col2]:
       # del row
        
#feature.apply (lambda row: drop_unmatched (row,'id','Track_ID'),axis=1)

##combine and clean the two raw datasets
#feature = feature.reset_index(drop=True)
#del feature['Trackname']
##combine two datasets
colnames=['Track_name','Track_ID','Album_name','Album_ID','Movie_name','Movie_genre','Movie_gross','Movie_rate','Movie_runtime','Movie_vote','Movie_yr']
titles.columns=colnames
for col in colnames:
    feature[col]=titles[col]

##remove rows with unmatched track ids
#for i in feature:
    #if i['id']!=i['Track_ID']:
      #  feature.drop(i)


#del featurelist['Trackname']
#titles=titles[:200]
##combine titles with featurelist 
#getfeature=pd.read_csv('featurelist.csv',sep = ',', encoding ='latin1')
#getfeature['here']=['sge']*len(getfeature)
##remove useless column
#col_tobedel=['analysis_url','id','track_href','type','uri','track_id','Movie_vote']


#for i in col_tobedel:
    #del feature[i]
    
##remove duplicated rows
def duplicated_rows(df):
    '''this function is to remove duplicated rows
    '''
    dr=df.loc[df.duplicated(keep='first')]
    newdf=df.drop(df.index[dr.index])
    return newdf

##remove empty rows
feature=duplicated_rows(feature)
feature.dropna()
#features=duplicated_rows(getfeature)
#def quality_check(df):
    '''function to check the quality of cleanness on the whole dataset
    '''
    #df.duplicated(keep='first')
    
    ##drop empty rows
##check range of each column
#def range_check(df):
    '''this function is written to check whether there exist illegal values 
    in each column
    '''
filtered_data = feature.dropna(axis='rows', how='any')
filename='full_dataset.csv'
filtered_data.to_csv(filename, sep = ',',encoding='utf-8-sig', mode='a', index = False, float_format='%.8f')


