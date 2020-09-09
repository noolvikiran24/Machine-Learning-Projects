#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 19:37:04 2019

@author: kirannoolvi
"""

import numpy as np
#import pandas as pd
import re
import sys


def preprocessing(tweet):
    tweet = tweet.lower() #Converted the tweet to lower case tweet
    #tweet = re.sub(r’\d+’, ‘’, tweet) # Remove numbers from the tweets
    tweet = re.sub(r'[^a-zA-Z0-9\s]', '', tweet)# Remove punctuation from the tweet
    tweet = tweet.strip() #Remove white space from the tweet
    tweet = re.sub(r'(\s)@\w+', r'\1', tweet) # Remove words starting with @
    tweet = re.sub(r"http\S+", "", tweet)  #Remove url
    return tweet

#print(preprocessing('Planning to hire a personal trainer? Read these 7 tips first: http://ow.ly/LpxFq'))
terms = {}


file=open('usnewshealth.txt',encoding="utf8") #Get the tweets data from text file
j=0
for line in file.readlines():
    splittweets=line.split("|") #Get the tweets
    tweet = splittweets[2]
    terms[j]=preprocessing(tweet)
    j=j+1


initial_seeds = [] 

k = input("Enter K: ") #Take the value of k

initial_seeds=np.random.randint(low=0, high=len(terms)-1, size=int(k)) #Take some random tweets in the initial list

print("Initial Centroids:")
print(initial_seeds)

def jaccard(a,b):
    
    a = a.split(" ")
    b = b.split(" ")
    setA = set(a)
    setB = set(b)
    a_U_b = len(setA.union(setB))
    a_I_b = len(setA.intersection(setB))    
    result = 1 - (a_I_b/a_U_b)
    return result

while True:
    tweetcluster={}
     
    for centroid in initial_seeds:
        tweetcluster[centroid]=[]
        
    for id,tw in terms.items():#Formation of clusters
        mincentroid=tweetcluster[initial_seeds[0]]
        mind = sys.maxsize
        for centroid in initial_seeds:
            distance = jaccard(terms[centroid],tw)
            if(distance < mind):
                mind = distance
                mincentroid = centroid
        tweetcluster[mincentroid].append(id)
                     
    newCentroids=[] 
    
    for id,tw in tweetcluster.items():  #Centroids updating
        mind=sys.maxsize
        min_centroid=id
        for tweet1 in tweetcluster[id]:
            distance=0
            for tweet2 in tweetcluster[id]:
                distance=distance+jaccard(terms[tweet1], terms[tweet2])
            mean=distance/len(tweetcluster[id])
            if mean<mind:
                mind=mean
                min_centroid=tweet1
        newCentroids.append(min_centroid)
    
    if set(newCentroids) == set(initial_seeds):#check if the the centroids formed are equal to the previous one, If yes break
        break
    else:
        initial_seeds=newCentroids.copy()
      
SSE=0 #Intialize SSE
for centroid_id in tweetcluster:

    for tweetId in tweetcluster[centroid_id]:
        ssedistance=(jaccard(terms[centroid_id],terms[tweetId]) **2)
        SSE += (ssedistance*ssedistance) 
print("SSE: "+str(SSE))                
              
print("Final Centroids: ")    
print(initial_seeds)

no=1
for centroid_id in initial_seeds:
    print(str(no)+"->Cluster Id:  "+ str(centroid_id) +", No of Tweets: " + str(len(tweetcluster[centroid_id])))
    no+=1

