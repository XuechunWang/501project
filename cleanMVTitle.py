# -*- coding: utf-8 -*-
"""
Created on Wed Oct  3 13:54:30 2018

@author: LY
"""
import pandas as pd
import re
import unidecode as uni


# read in data
mvData = pd.read_csv('mv.csv', sep = ',', encoding ='utf-8')
#print(mvData[:10])

# convert the title column into a list 
titleLst = mvData['title'].tolist()
#print(type(titleLst))
#print(titleLst[:10])
# convert all the movie titles into a long string to better use regular expression
# use '#' to join diffrent movies so that it's easy to split or combine later
titleStr = '#'.join(titleLst)
#print(type(titleStr))
#print(titleStr[:100])

################### 
##fix '&amp;'
################### 
# When we scrape movie titles from the IMDB webpage, 
# somehow, the '&' becomes '&amp;'. To facilitate our search later,
# we decide to replace '&amp;' with 'and'

ampPattern = re.compile(r'\&[amp]+\;')
(cleanTitleStr, n) = (re.subn(ampPattern,'and',titleStr))
#print(re.findall(ampPattern,failMV_3))
#print("The number of '&amp;' replaced by 'and':", n)
titleClean = cleanTitleStr.split('#')
#print(type(titleClean))
#print(titleClean[:10])
mvData['titleClean'] = titleClean
#print(mvData[:10])

# create a movie title column specifically for query in Spotify

undesiredPattern = re.compile(r'[^a-zA-Z0-9\s\#]')
#print(set(re.findall(undesiredPattern,cleanTitleStr)))

######################################  
## fix special letters with accent
## such as 'ô', 'é'
######################################
cleanTitleStr_2 = uni.unidecode(cleanTitleStr)
#print(cleanTitleStr_2)
#print(set(re.findall(undesiredPattern,cleanTitleStr_2)))


#########################################################  
## fix movie titles with roman numbers in it
#########################################################
 
# It turns out that we cannot obtain the corresponding soundtrack album
# on Spotify through the full name with roman numbers, which indicates the 
# order in the movie series, such as 'The Godfather: Part II' or
# 'Star Trek VI: The Undiscovered Country'
# We need to keep only 'The Godfater' or 'Star Trek The Undiscovered Country'
# in order for a result on Spotify
romanNum = re.compile(r'.*\s+[VI" "]+')
#print(re.findall(romanNum,newMV))
#print(len(re.findall(romanNum,newMV)))

# split the long string into individual movie names
tempMV =cleanTitleStr_2.split('#')
#print(len(tempMV))
# return movie names part of which contains roman number pattern
romanNumMV = [movie for movie in tempMV if re.search(romanNum, movie) is not None]
#print(romanNumMV[:])
#print(len(romanNumMV))

# After printing out the filtered movie names, we may note that  
# it's not easy to capture only the movie names with roman numbers in it.
# Though it might be possible to come up with a regular expression
# that works perfectly well, it's way too trivial.
# We decide to fix these one by one.

romanNumList = ['Episode VIII', 'Vol. I','Part II','II','Part III','Episode III',
                ' Episode V','Vol. 2','Episode VI','VI', 'Part 1',' II','Episode I',
                'chapter 2','Chapter 2','Vol. 1', ': I ',':I ', 'IV']
# replace roman number part with space
cleanTitleLst_3 = []    
for title in tempMV:
    for romanNum in romanNumList:
        if all(list(map(lambda x: x in list(title), list(romanNum)))): 
            title = title.replace(romanNum, '')            
        else:
            continue
    cleanTitleLst_3.append(title)
#print(cleanTitleLst_3)[:10]

###########################
## fix special characters
###########################
# since white space works well in our search, 
# we decide to replace all the special characters found
# with the white space

undesiredChars = set(re.findall(undesiredPattern, '#'.join(cleanTitleLst_3)))
#print(undesiredChars)

# this variable is to store the clean version of movie titles for Spotify search
cleanTitleSpot = []
# loop through every movie title and replace undesired chars with the space
for mv in cleanTitleLst_3:
    for undesiredChar in undesiredChars:
        if undesiredChar in list(mv):
            mv = mv.replace(undesiredChar, '')
    cleanTitleSpot.append(mv)
#print(cleanTitleSpot)
#print(len(cleanTitleSpot))

# add a new column to the original data frame 
mvData['cleanTitleSpot'] = cleanTitleSpot

# create a new output file 
with open('cleanMVData.csv','w',encoding='utf-8') as f:
    mvData.to_csv(f, sep=',', index = False)
    

    

