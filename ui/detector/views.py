from django.shortcuts import render

from django.http import HttpResponseRedirect, HttpResponse
from .forms import NameForm

import nltk
import json
import numpy as np
from nltk import FreqDist, ngrams
import numpy as np
import loader
import sklearn
from nltk.tokenize import word_tokenize
from Model import MLModel

        
model = MLModel()

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
                                X[m,nModel*k] = X[m,nModel*k] + np.log(language_dist[language]['words'][1].freq(words)) 
                            if count > 0:                              
                                if (word1,words)  in keys2:
                                    X[m,1+nModel*k] = X[m,1+nModel*k] + np.log(language_dist[language]['words'][2].freq((word1,words)))
                                word1=words
                            if (count > 1): 
                                if (word11,word21,words) in keys3:
                                    X[m,2+nModel*k] = X[m,2+nModel*k] + np.log(language_dist[language]['words'][3].freq((word11,word21,words)))   
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
    
def train():
    LANGUAGES=list(set(['fr','es','ru']))
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
    
    print("Computing number of words")
    NumbersWords=np.zeros((3,5))
    for i in range(0,n):
        j=0
        for language in LANGUAGES:
            NumbersWords[i,j]=sum(language_dist[language]['words'][i+1].values())
            j=j+1
    #print NumbersWords
    #training features
    print ("Starting loaderShuffleData")
    trainData=loader.loaderShuffleData()
    print ("computing X and Y matrices")
    computeFeatures(trainData,language_dist,LANGUAGES,0)
    return language_dist


def index(request):
    #return HttpResponse("Hello, world. You're at the polls index.")
#    if request.method == 'POST':
#        form = NameForm(request.POST)
#        if form.is_valid():
#            content = form.cleaned_data #['your_text']
#            return HttpResponse(content)
#            #return HttpResponseRedirect('detector/classify.html')
#    else:
    form = NameForm()
    return render(request, 'detector/text_form.html', {'form':form})
    
def classify_with_model(content):
    if model.first_run == True:
        model.first_run = False
        model.language_dist = train()
        X=np.loadtxt('X.txt')
        Y=np.loadtxt('Y.txt')
        model.weights = SVM(X,Y,3,3)
    comment = word_tokenize(content)
    Ypredict= model.weights.predict(model.language_dist, comment)      
        
    if Ypredict==0:
       return "French"
    if Ypredict==1:
        return "Spanish"
    else:
        return "Russian"
    
def classify(request):
    if request.method == 'POST':
        form = NameForm(request.POST)
        if form.is_valid():
            content = classify_with_model(form.cleaned_data['your_text'])            
    
    return render(request, 'detector/detected.html', {'content': content})


