# -*- coding: utf-8 -*-
"""
Created on Thu Oct  4 10:26:18 2018

@author: youko
"""

##this .py file is used for cleaning the scraped raw data
##read the files
titles=pd.read_csv('tracklist.csv',sep=',',encoding='utf-8-sig')
##reset index 
feature = featurelist.reset_index(drop=True)
del feature['Trackname']
##combine two datasets
colnames=['Track_name','Track_ID','Album_name','Album_ID','Movie_name','Movie_genre','Movie_gross','Movie_rate','Movie_runtime','Movie_vote','Movie_yr']
titles.columns=colnames
for col in colnames:
    feature[col]=titles[col]

##remove rows with unmatched track ids
#for i in feature:
    #if i['id']!=i['Track_ID']:
      #  feature.drop(i)
def drop_unmatched(row,col1,col2):
    if row[col1] != row[col2]:
        del row
        
feature.apply (lambda row: drop_unmatched (row,'id','Track_ID'),axis=1)

#del featurelist['Trackname']
#titles=titles[:200]
##combine titles with featurelist 
#getfeature=pd.read_csv('featurelist.csv',sep = ',', encoding ='latin1')
#getfeature['here']=['sge']*len(getfeature)
##remove useless column
#col_tobedel=['analysis_url','id','track_href','type','uri','track_id','Movie_vote']
del feature['analysis_url']
del feature['id']
del feature['track_href']
del feature['type']
del feature['uri']

del feature['track_id']
del feature['Movie_vote']

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
filtered_data = feature.dropna(axis='columns', how='all')
filtered_data = filtered_data.dropna(axis='rows', how='any')
filename='full_dataset.csv'
filtered_data.to_csv(filename, sep = ',',encoding='utf-8-sig', mode='a', index = False, float_format='%.8f')



