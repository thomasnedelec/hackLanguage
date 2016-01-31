# -*- coding: utf-8 -*-
"""
Created on Sat Jan 30 16:12:20 2016

@author: danio
"""
import nltk
import json
import numpy as np
from nltk import FreqDist, ngrams
import numpy as np
import loader
from sklearn import svm
import sklearn

def loadData(language):
    url1='jsons/User_'+language  
    url=url1+'-N.json'
    json_data = open(url).read()
    data = json.loads(json_data)
    return data

def writeToFile(X, filename):
    np.savetxt(filename,X, fmt="%4.4f")

def computeFeatures (trainData,language_dist,LANGUAGES,test):
    nLanguages=3
    nModel=3

    numberComments=20000
    mapLanguage={}
    values=0
    for language in LANGUAGES:
        mapLanguage[language]=values
        values=values+1
    #print mapLanguage    
    X=np.zeros((numberComments,nLanguages*nModel))
    Y=np.zeros((numberComments))
    for m in range(numberComments):
        if (m < numberComments):
            if (m  % 100 == 0):
                print m 
                
            entry=trainData[m]
            k=0
            for language in LANGUAGES:

                    #print(language_dist[language]['words'][j+1].N())
                    #print(language_dist[language]['words'][j+1].max())
                    #print(language_dist[language]['words'][j+1].max())
                    #print(sentence)
                    #print(language_dist[language]['words'][j+1].N())
                    if len(entry[0])>2:
                        word1=entry[0][0]
                        word11=entry[0][0]
                        word21=entry[0][1]
                        keys = language_dist[language]['words'][1].keys()
                        keys2=language_dist[language]['words'][2].keys()
                        keys3=language_dist[language]['words'][3].keys()
                        count=0
                        for words in entry[0]:
                            if count < 25: 
                                if words in keys:
                                    X[m,nModel*k]=X[m,nModel*k]+np.log(language_dist[language]['words'][1].freq(words)) 
                                if count > 0:
                                    
                                    if (word1,words)  in keys2:
                                        X[m,1+nModel*k]=X[m,1+nModel*k]+np.log(language_dist[language]['words'][2].freq((word1,words)))
                                    word1=words
                                if (count > 1): 
                                    if (word11,word21,words) in keys3:
                                        X[m,2+nModel*k]=X[m,2+nModel*k]+np.log(language_dist[language]['words'][3].freq((word11,word21,words)))   
                                    word11=word21
                                    word21=words
                                count=count+1
                        k=k+1
            Y[m]=mapLanguage.get(entry[1])
            #print(1)
        
            m=m+1
            
    if test==0:
        writeToFile(X,"X.txt")
        writeToFile(Y,"Y.txt")
    else:
        writeToFile(X,"Xtest.txt")
        writeToFile(Y,"Ytest.txt")
    
def SVM(X,Y,nLanguage,nModel):
    weights=np.zeros(nLanguage*nModel)
    svc=sklearn.svm.SVC()   
    weights=svc.fit(X,Y)
    print(weights)
    return weights
    
if __name__ == '__main__':
    LANGUAGES=list(set(['fr','en','ru']))
    #LANGUAGES = list(set(['ru', 'en-us', 'de','yue','fr']))
    n = 3
    nLanguages=3
    language_dist = {}
    for language in LANGUAGES:
        data = loadData(language)
        language_dist[language] = {"words": dict(zip(range(1, n+1), [FreqDist() for i in range(1, n+1)])),
                               "chars": dict(zip(range(1, n+1), [FreqDist() for i in range(1, n+1)]))
                              }
        
        z = 0        
        for entry in data:
                if z <25:
                    #for words in entry['text']:
                    for i in range(1, n+1):
                    #print(words)
                    #print(nltk.ngrams(words,i))
                        if i==1:
                            language_dist[language]['words'][i].update([key[0] for key in nltk.ngrams(entry['text'], 1)])
                        else:
                           language_dist[language]['words'][i].update(nltk.ngrams(entry['text'], i)) 
                z=z+1
        #print language_dist[language]["words"][1].max()
    
#    print("Computing number of words")
#    NumbersWords=np.zeros((3,5))
#    for i in range(0,n):
#        j=0
#        for language in LANGUAGES:
#            NumbersWords[i,j]=sum(language_dist[language]['words'][i+1].values())
#            j=j+1
#    #print NumbersWords
#    #training features
#    print ("Starting loaderShuffleData")
#    trainData=loader.loaderShuffleData()
#    print ("computing X and Y matrices")
#    computeFeatures(trainData,language_dist,LANGUAGES,NumbersWords,0)
    print("implementing SVM ranking")
    X=np.loadtxt('Xtrain.txt')
    Y=np.loadtxt('Ytrain.txt')
    weights=SVM(X,Y,nLanguages,n)
    developmentData=loader.loaderShuffleDataTest()
    computeFeatures(developmentData,language_dist,LANGUAGES,1)
    X=np.loadtxt('Xtest.txt')
    Y=np.loadtxt('Ytest.txt')
    nbPrediction=len(Y)    
    Ypredict=weights.predict(X)
    precision=0
    nCorrect=0
    for i in range(len(Y)):
        if Ypredict[i]==Y[i]:
            nCorrect=nCorrect+1
            
    precision=nCorrect/len(Y)
    print("Precision is equal to "+str(precision)+"on "+str(nbPrediction)+" comments")
#    LANGUAGES = list(set(['english', 'french', 'german']))
#    for language in LANGUAGES:
##    language_dist[language] = {"words": dict(zip(range(1, n+1), [FreqDist() for i in range(1, n+1)])),
##                               "chars": dict(zip(range(1, n+1), [FreqDist() for i in range(1, n+1)])),
##                               "w_sizes": dict(zip(range(1, n+1), [FreqDist() for i in range(1, n+1)]))}
##   
#   json_data = open('User_de-N.json').read()
#   data = json.loads(json_data)
#
#
#   for entry in data['User_de-N']:
#       for words in entry['text']:
#           print words
        #language_dist[language]["words"][i].update(nltk.ngrams(words, i))
        #language_dist[language]["chars"][i].update(nltk.ngrams(statement_text, i))

                
        #print entry['level']
#    print data
    #language_distribution(2,)
    #train = extra