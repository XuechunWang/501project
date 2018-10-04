# -*- coding: utf-8 -*-
"""
Created on Tue Oct  2 00:37:58 2018

@author: LY
"""

from bs4 import BeautifulSoup, SoupStrainer
import requests
import re
import numpy as np
import pandas as pd
import time 

## first page of the desired advanced searching results 
# https://www.imdb.com/search/title?title_type=feature&user_rating=7.0,10.0
# &num_votes=20000,&has=soundtracks&count=250&view=simple
def scrpIMDB():
    # basic url
    myURL = 'https://www.imdb.com/search/title'
    
    # basic query
    queryBsc = ('title_type=feature'
             '&user_rating=7.0,10.0'
             '&num_votes=20000,'
             '&has=soundtracks'
             '&count=250')

    (title1,runtime1,genre1,yr1,rate1,vote1,gross1) = scrpFirstPage(myURL, queryBsc)
    (title2,runtime2,genre2,yr2,rate2,vote2,gross2) = scrpNxtPage(myURL, queryBsc)

#    merge 
    title = title1 + title2
    runtime = runtime1 + runtime2
    genre = genre1 + genre2
    yr = yr1 + yr2
    rate = rate1 + rate2
    vote = vote1 + vote2
    gross = gross1 + gross2
#    print('Sample movie links\n')
#    print('First three scraped:')

    mvDF = pd.DataFrame({'title':title,
                         'runtime':runtime,
                         'genre':genre,
                         'yr':yr,
                         'rate':rate,
                         'vote':vote,
                         'gross':gross
                         })
    print(mvDF[:10])
    with open('mv.csv','w',encoding='utf-8') as f:
        mvDF.to_csv(f, sep=',', index = False)
#    title1 = scrpFirstPage(myURL, queryBsc)
#    title2 = scrpNxtPage(myURL, queryBsc)
#    title = title1 + title2
#    print(title[:3])#    title1 = scrpFirstPage(myURL, queryBsc)
#    title2 = scrpNxtPage(myURL, queryBsc)
#    title = title1 + title2
#    print(title[:3])
#        with open('mvtitle.txt','w',encoding='utf-8') as f:
#        titleDF.to_csv(f, sep='\t')
    
#    print('Last three scraped:')
#    print(mvLinksAll[-3:])
#    print("Total movies available:")
#    print(len(mvLinks))
#    print(len(runtime))
#    print(len(genre))
#    print(len(yr))
#    print(len(rate))
#    print(len(vote))
#    print(len(gross))


def scrpFirstPage(myURL, query):

    # set timeout parameter to wait for 10s for the server to response
    response = requests.get(myURL, query, timeout = 10)
#    title1 = getMVTitle(response)
#    return title1
    title1 = getTitle(response)
    (runtime1,genre1,yr1) = getTimeGenYr(response)
    rate1 = getRate(response)
    (vote1,gross1) = getVoteGross(response)
    return (title1,runtime1,genre1,yr1,rate1,vote1,gross1)

## sample movie title links:
## <a href="/title/tt4154756/?ref_=adv_li_tt">Avengers: Infinity War</a>
## <a href="/title/tt5052474/?ref_=adv_li_tt">Sicario: Day of the Soldado</a>
## <a href="/title/tt3104988/?ref_=adv_li_tt">Crazy Rich Asians</a>
def getTitle(response):
    # within the response content, parse only <a> tage with href (hyperlink reference)
    soup = BeautifulSoup(response.text,'lxml', parse_only = SoupStrainer('a', href = True))
    # compile movie title links patterns using regular expression
    titleLinkPattern = re.compile(r"^\/title.+ref_=adv_li_tt$")
    # among all the links, only search for movie titles links 
    mvLinks = soup.find_all('a', {'href': titleLinkPattern})
    title = []
    titlePattern = re.compile(r'\>.+\/')
    for mvLink in mvLinks:
        title.append(re.search(titlePattern,str(mvLink)).group().strip('\>/<'))
    #print(title[:3])
    # each page lists 250 movies (except for the last one), 
    # thus the collected movie links per page should be 250
    # check if it's right 
    # linkcnt  = len(mvLinks)
    # print("Number of Scraped Movie Links in the page: ", linkcnt)
    #print(mvLinks[:3])
    return title

def getTimeGenYr(response):    
    # get runtime and genre
    ### sample html for runtime and genre
    #<p class="text-muted ">
    #            <span class="certificate">PG-13</span>
    #                 <span class="ghost">|</span> 
    #                <span class="runtime">149 min</span>
    #                 <span class="ghost">|</span> 
    #            <span class="genre">
    #Action, Adventure, Fantasy            </span>
    #    </p>
    soup1 = BeautifulSoup(response.text,'lxml', parse_only = SoupStrainer('span'))  
    
    
    # get runtimes
    runtimes = soup1.find_all(name = 'span',attrs={'class':'runtime'})
    runtime = [runtime.get_text() for runtime in runtimes]
#    print(runtime[:10])
#    print(runtime[-10:])
#    print(len(runtime))
    
    # get genres
    genres = soup1.find_all(name = 'span',attrs={'class':'genre'})
    genre = [genre.get_text().strip('\n\, ') for genre in genres]
#    print(genre[:10])
#    print(genre[-10:])    
#    print(len(genre))
    
    # get years
    # sample html for years
    #<span class="lister-item-year text-muted unbold">(I) (2016)</span>
    yrs = soup1.find_all(name = 'span',attrs={'class':'lister-item-year text-muted unbold'})
    yr = [yr.get_text().strip('( )I') for yr in yrs]
#    print(yr[:10])
#    print(yr[-10:])    
#    print(len(yr))
    return (runtime,genre,yr)    

def getRate(response):
    # get rates  
    # sample html <strong>8.6</strong>
    soup2 = BeautifulSoup(response.text,'lxml', parse_only = SoupStrainer('strong'))
    rates = soup2.find_all(name ='strong')
    rateStrs = [str(rate).strip('</strong> ') for rate in rates] 
    rate = []
    for rateStr in rateStrs:
        try:
            rateFlt = float(rateStr)
            if (rateFlt >= 7) & (rateFlt <= 10):
                rate.append(rateFlt)
        except:
            pass
#    print(rate[:10])
#    print(rate[-10:])
#    print(len(rate))
    return rate       


def getVoteGross(response):        
    # get votes and gross
    # sample html for votes and gross
#    <p class="sort-num_votes-visible">
#                <span class="text-muted">Votes:</span>
#                <span name="nv" data-value="493959">493,959</span>
#    <span class="ghost">|</span>                <span class="text-muted">Gross:</span>
#                <span name="nv" data-value="678,815,482">$678.82M</span>
#        </p>            
            
    soup3 = BeautifulSoup(response.text,'lxml', parse_only = SoupStrainer('p')) 
    votesGrosses = soup3.find_all('p',attrs={'class':'sort-num_votes-visible'})
    vote = []
    gross = []
    
    # use regular expressions to extract grosses and votes
    grossPattern = re.compile(r'\$\d+\.\d+M')
    votePattern = re.compile(r'"\d+"') # though this pattern possibly 
    # mathches both the votes and the gross, we use re.match(), which 
    # returns only the first string that matches it and votes always
    # comes before grosses according to the web page layout, if grosses exist.
    
    # loop through every elements 
    for element in votesGrosses:
        # if gross value exists
        if re.search(grossPattern, str(element)):
            # append it to the gross list
            gross.append(re.search(grossPattern, str(element)).group())
        # otherwise, append 'None'
        else: 
            gross.append('None')
        # find the number of votes, strip it to get rid of quotes
        # and transfer it to integer
        vote.append(int(re.search(votePattern, str(element)).group().strip('""')))   
#    print(gross[:10])
#    print(gross[-10:])    
#    print(len(gross))
#    print(vote[:10])
#    print(vote[-10:])    
#    print(len(vote))
    return (vote,gross)


## Go to the next page
# https://www.imdb.com/search/title?title_type=feature&user_rating=7.0,10.0
# &num_votes=20000,&has=soundtracks&count=250&view=simple&page=2&ref_=adv_nxt

# https://www.imdb.com/search/title?title_type=feature&user_rating=7.0,10.0
# &num_votes=20000,&has=soundtracks&count=250&view=simple&page=3&ref_=adv_nxt

def scrpNxtPage(myURL, query):
    # starting from page 2
    pageNum = 2
    # Read the number of available movies after filters from the web page
    avlNum = 2122
    # 250 is the number of listed movies per page, 
    cnt = 250
    title2,runtime2,genre2,yr2,rate2,vote2,gross2 = [],[],[],[],[],[],[]
    # while page number less than the total pages available,
    # scrape the page
    while pageNum <= np.ceil(avlNum / cnt) :
        queryNxt = ('&page=' + str(pageNum) + '&ref_=adv_nxt')
        responseNxt = requests.get(myURL, query + queryNxt, timeout = 10)
        # join all the movie links list, attributes lists together using '+'
        print('Page ' + str(pageNum) + '...')
        title2 += getTitle(responseNxt)
        runtime2 += getTimeGenYr(responseNxt)[0]
        genre2 += getTimeGenYr(responseNxt)[1]
        yr2 += getTimeGenYr(responseNxt)[2]
        rate2 += getRate(responseNxt)
        vote2 += getVoteGross(responseNxt)[0]
        gross2 += getVoteGross(responseNxt)[1]
        
        pageNum += 1
        time.sleep(10)
    return (title2,runtime2,genre2,yr2,rate2,vote2,gross2)




scrpIMDB()

